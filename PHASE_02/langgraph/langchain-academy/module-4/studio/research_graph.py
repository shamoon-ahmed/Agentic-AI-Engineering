from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field
from langgraph.types import Send

from typing_extensions import TypedDict
from langchain.messages import HumanMessage, SystemMessage

from langgraph.graph import END
from langchain.messages import AIMessage
from langgraph.checkpoint.memory import MemorySaver

import operator
from typing import Annotated, List
from langchain_tavily import TavilySearch
from langgraph.graph import StateGraph, START, END

from langgraph.graph import MessagesState
import wikipedia
from langchain_community.document_loaders import WikipediaLoader
from langchain_core.messages import SystemMessage
from langchain_core.messages import get_buffer_string

load_dotenv()

llm = init_chat_model(model="gpt-5-nano")

class Analyst(BaseModel):
    name : str = Field(description="Name of analyst")
    role : str = Field(description="Role of the analyst based on the context of topic")
    description : str = Field(description="Description of the analyst's focus, motives and concerns")

    @property
    def persona(self) -> str:
        return f"Name: {self.name}, Role: {self.role}, Description: {self.description}"

class GenerateAnalyst(TypedDict):
    topic: str
    max_num_analyst : int
    human_fb: str
    analysts : List[Analyst]

class ExpertInterviewState(MessagesState):
    analyst : Analyst
    max_num_questions : int
    context : Annotated[list, operator.add]
    sections: list
    interview : str

class ResearchGraphState(TypedDict):
    topic: str
    max_num_analyst : int
    human_fb: str
    analysts : List[Analyst]
    sections: Annotated[list, operator.add]
    introduction : str
    content : str
    conclusion : str
    final_report : str

class AnalystsList(BaseModel):
    analysts : List[Analyst] = Field(description="List of analysts")

class SearchQuery(BaseModel):
    search_query: str = Field(description="an appropriate wording for search")


create_analyst_instructions = """Create {max_num_analysts} research analysts for the topic: {topic}. If theres a human feedback, work according to the human feedback: {human_fb}"""

# node
def create_analysts(state: GenerateAnalyst):
    topic = state["topic"]
    num_of_analysts = state["max_num_analyst"]
    human_feedback = state.get('human_fb', '')

    system_prompt = create_analyst_instructions.format(max_num_analysts=num_of_analysts, topic=topic, human_fb=human_feedback)
    generated_analysts = llm.with_structured_output(schema=AnalystsList).invoke(
        [SystemMessage(content=system_prompt)]+[HumanMessage(content="generate 3 analysts based on the topic provided")])

    return {"analysts": generated_analysts.analysts}

# node
def human_feedback(state: GenerateAnalyst):
    pass

question_instructions = """

this is your persona: {persona}

ask 2-3 deep question required for the research

dont be too lengthy. be precise

When you're satisfied, say : Thank you so much for your time
"""

# node
def ask_question(state: ExpertInterviewState):

    analyst = state["analyst"]
    messages = state["messages"]

    prompt = question_instructions.format(persona=analyst.persona)
    llm_output = llm.invoke([SystemMessage(content=prompt)]+messages)

    return {"messages": [llm_output]} # output should be a list


search_instructions = """You will be given a conversation between an analyst and an expert.

Your goal is to generate a concise 3-to-6 word search query for retrieval and Wikipedia.

Guidelines:
1. Keep the query short (3 to 6 words).
2. NEVER use boolean operators like AND, OR, NOT.
3. NEVER use complex punctuation, quotes, or semicolons.
4. Focus on the core entity or concept (e.g., "AI ethics framework" or "Artificial intelligence in healthcare")."""

# node
def search_internet(state: ExpertInterviewState):

    messages = state["messages"]

    tavily_client = TavilySearch(max_results=3)

    search_prompt = llm.with_structured_output(SearchQuery).invoke([SystemMessage(content=search_instructions)]+messages)

    search = tavily_client.invoke({"query":search_prompt.search_query})
    results = search.get("results", search)

    formatted_search_docs = "\n\n---\n\n".join(
        [
            f'<Document href="{doc["url"]}"/>\n{doc["content"]}\n</Document>'
            for doc in results
        ]
    )

    return {"context":[formatted_search_docs]}


# 1. Set a custom User-Agent (Wikipedia blocks the default Python requests header)
wikipedia.set_user_agent("ResearchAgentBot/1.0 (https://github.com/my-project; research@example.com)")

def search_wikipedia(state: ExpertInterviewState):
    """Retrieve docs from wikipedia safely"""
    
    # 2. Extract search query using structured output
    structured_llm = llm.with_structured_output(SearchQuery)
    search_query = structured_llm.invoke([SystemMessage(content=search_instructions)] + state['messages'])
    
    query = ""
    if search_query and hasattr(search_query, "search_query") and search_query.search_query:
        query = search_query.search_query.strip()

        for noise in [" AND ", " OR ", " NOT ", '"', "(", ")", ";"]:
            query = query.replace(noise, " ")
        # Keep only the first 5-6 words
        query = " ".join(query.split()[:6])
    
    if not query:
        return {"context": []}

    # 3. Query Wikipedia inside a guarded try-except block
    try:
        search_docs = WikipediaLoader(
            query=query, 
            load_max_docs=2
        ).load()

        if not search_docs:
            return {"context": [f"<Document source='Wikipedia'>No articles found for: {query}</Document>"]}

        formatted_search_docs = "\n\n---\n\n".join(
            [
                f'<Document source="{doc.metadata.get("source", "Wikipedia")}" page="{doc.metadata.get("page", "")}"/>\n{doc.page_content}\n</Document>'
                for doc in search_docs
            ]
        )
        return {"context": [formatted_search_docs]}

    except Exception as e:
        print(f"Wikipedia search failed for '{query}': {e}")
        # Return fallback context so the Expert node still has search data to proceed with
        return {"context": [f"<Document source='Wikipedia'>Wikipedia search unavailable for: {query}</Document>"]}


answer_instructions = """
you are being interviewed by an analyst

the analyst's persona is this: 
Analyst Persona:
{persona}

make sure you answer questions properly based on this context provided to you:
Context:
{context}
"""

# node
def generate_answer(state: ExpertInterviewState):

    messages = state["messages"]
    context = state["context"]
    analyst = state["analyst"]

    prompt = answer_instructions.format(persona=analyst.persona, context=context)

    answer = llm.invoke([SystemMessage(content=prompt)] + messages)

    answer.name = "expert"

    return {"messages": [answer]}


# node
def save_interview(state: ExpertInterviewState):

    messages = state["messages"]

    interview_content = get_buffer_string(messages)

    return {"interview": interview_content}

# conditional edge
def should_continue_interview(state: ExpertInterviewState, name: str = "expert"):
    
    messages = state["messages"]
    max_num_questions = state.get("max_num_questions", 2)

    msgs_len = len(
        [m for m in messages if isinstance(m, AIMessage) and m.name==name]
    )

    last_message = messages[-2]

    if msgs_len >= max_num_questions:
        return "save_interview"
    
    if "Thank you so much for your time" in last_message.content:
        return "save_interview"
    
    return "ask_question"


section_writing_instructions = """
you are a very good section/memo writer who will write a report on this analyst and expert conversation

DO NOT MAKE A VERY LONG REPORT! make sure it is under 3000 words

this is the context that is provided to you if it helps:

Context:
{context}

the section titile and theme should be based on this description:
Description: {description}

analyze it first fully and then write a summarized memo/section but do not miss any important information or details

DO NOT MAKE A VERY LONG REPORT! make sure it is under 3000 words
"""

def write_section(state: ExpertInterviewState):

    context = state["context"]
    analyst = state["analyst"]
    interview = state["interview"]

    prompt = section_writing_instructions.format(context=context, description=analyst.description)
    section = llm.invoke([prompt]+[HumanMessage(content=f"""
    write the summarized section based on the context provided and this interview:
    Interview:
    {interview}
    """)])

    return {"sections":[section.content]}

interview_graph = StateGraph(ExpertInterviewState)
interview_graph.add_node("ask_question", ask_question)
interview_graph.add_node("search_internet", search_internet)
interview_graph.add_node("search_wikipedia", search_wikipedia)
interview_graph.add_node("generate_answer", generate_answer)
interview_graph.add_node("save_interview", save_interview)
interview_graph.add_node("write_section", write_section)

interview_graph.add_edge(START, "ask_question")
interview_graph.add_edge("ask_question", "search_internet")
interview_graph.add_edge("ask_question", "search_wikipedia")
interview_graph.add_edge("search_internet", "generate_answer")
interview_graph.add_edge("search_wikipedia", "generate_answer")
interview_graph.add_conditional_edges("generate_answer", should_continue_interview, ["save_interview", "ask_question"])
interview_graph.add_edge("save_interview", "write_section")
interview_graph.add_edge("write_section", END)

def initiate_interviews(state: ResearchGraphState):

    human_approval = state.get('human_fb', "approve")

    if human_approval != "approve":
        return "create_analysts"
    
    else:
        topic = state["topic"]
        return [
            Send("conduct_interview", {
                "max_num_questions": 2,
                "analyst":a,
                "messages":[HumanMessage(content=f"so you were writing a section on {topic}")]
            }) for a in state["analysts"]
        ]


write_report_instructions = """
you are tasked with writing the middle part of the report by looking at the sections provided to you below

do not write a report of more than 3000 words.

this is the topic:
{topic}

and this are the sections:
{sections}
"""

def write_middle_report_content(state: ResearchGraphState):

    topic = state["topic"]
    sections = state["sections"]

    formatted_str_sections = "\n\n".join([f"{section}" for section in sections])

    instructions = write_report_instructions.format(topic=topic, sections=formatted_str_sections)
    report = llm.invoke([SystemMessage(content=instructions)] + [HumanMessage(content="write the middle part of report content as you have the topic and sections provided")])

    return {"content":report.content}

write_introduction_instructions = """
you are tasked with writing the intro of the report by looking at the sections provided to you below

make sure it is very brief and contains hook

this is the topic:
{topic}

and this are the sections:
{sections}
"""


def write_intro(state: ResearchGraphState):

    topic = state["topic"]
    sections = state["sections"]

    formatted_str_sections = "\n\n".join([f"{section}" for section in sections])

    instructions = write_introduction_instructions.format(topic=topic, sections=formatted_str_sections)
    intro = llm.invoke([SystemMessage(content=instructions)] + [HumanMessage(content="write the introduction as you have the topic and sections provided")])

    return {"introduction":intro.content}


write_conclusion_instructions = """
you are tasked with writing the conclusion of the report by looking at the sections provided to you below

make sure it is very brief and contains good precise conclusion

this is the topic:
{topic}

and this are the sections:
{sections}
"""


def write_conclusion(state: ResearchGraphState):

    topic = state["topic"]
    sections = state["sections"]

    formatted_str_sections = "\n\n".join([f"{section}" for section in sections])

    instructions = write_conclusion_instructions.format(topic=topic, sections=formatted_str_sections)
    conclusion = llm.invoke([SystemMessage(content=instructions)] + [HumanMessage(content="write the conclusion as you have the topic and sections provided")])

    return {"conclusion":conclusion.content}

def finalize_report(state: ResearchGraphState):

    intro = state["introduction"]
    middle_report_content = state["content"]
    conclusion = state["conclusion"]

    finalized_report = intro + "\n\n---\n\n" + middle_report_content + "\n\n---\n\n" + conclusion

    return {"final_report": finalized_report}

builder = StateGraph(ResearchGraphState)
builder.add_node("create_analysts", create_analysts)
builder.add_node("human_feedback", human_feedback)
builder.add_node("conduct_interview", interview_graph.compile())
builder.add_node("write_middle_report_content", write_middle_report_content)
builder.add_node("write_intro", write_intro)
builder.add_node("write_conclusion", write_conclusion)
builder.add_node("finalize_report", finalize_report)

builder.add_edge(START, "create_analysts")
builder.add_edge("create_analysts", "human_feedback")
builder.add_conditional_edges("human_feedback", initiate_interviews, ["conduct_interview", "create_analysts"])
builder.add_edge("conduct_interview", "write_intro")
builder.add_edge("conduct_interview", "write_middle_report_content")
builder.add_edge("conduct_interview", "write_conclusion")
builder.add_edge(["write_intro", "write_middle_report_content", "write_conclusion"], "finalize_report")
builder.add_edge("finalize_report", END)

research_graph = builder.compile(interrupt_before=["human_feedback"])
