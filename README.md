## How to use this tracker

- Mark each phase complete when you finish it.
- Under each phase, add what you learned, links, and mini-projects.
- Add dates if you want (start/end) next to the phase title.

---

## Roadmap milestones (6 phases)

### 🤖 Phase 1 — Python fluency + LLM API (Weeks 1–2)

- [ ]  **Complete Phase 1**
- **📅 Weeks:** 1–2 — *Python for AI + calling your first LLM API*
- **⏱️ Time:** ~2 weeks
- **📚 Learn (check off):**
    - [x]  **Python async/await — critical for AI APIs**   (July, 17, 2026)
        
        Almost every production AI API call is async. Most beginners skip this and break in deployment. Learn async def, await, `asyncio.run()`
        
    - [x]  **Python type hints and Pydantic** (July, 19, 2026)
        
        FastAPI and LangChain both heavily use type hints. Learn how to define data models with Pydantic BaseModel — this is a real job skill.
        
    - [x]  **Call the OpenAI / Anthropic API directly (no LangChain)** (July, 21, 2026)
        
        Using the raw API first teaches you what LangChain is actually abstracting. Build a simple chat loop, pass message history, handle streaming responses.
        
    - [ ]  **Prompt engineering fundamentals**
        
        System prompts, few-shot examples, chain-of-thought, ReAct prompting, structured output (JSON mode). These are job interview topics.
        
    - [x]  **Environment management — .env files, python-dotenv, virtual envs**
        
        Never hardcode API keys. Every job expects this. Use python-dotenv and .gitignore from day one.
        
- **🔗 Resources:**
    - [ ]  📗 **DeepLearning.AI — ChatGPT Prompt Engineering for Developers** (free, 1 hour, Andrew Ng + OpenAI)
    - [ ]  📗 **OpenAI API docs** — platform.openai.com/docs. Read the quickstart. Build the examples yourself.
    - [ ]  📗 **Anthropic API docs** — docs.anthropic.com. Try Claude API directly (more generous free tier for learning).
- **🏷️ Tags:**
    - Python 3.10+
    - openai SDK
    - anthropic SDK
    - python-dotenv
    - Pydantic
    - async/await
- **🛠️ Mini-project: CLI chatbot with memory**
    
    A command-line chatbot that maintains conversation history, uses a system prompt you wrote, and responds in a structured JSON format. Deploy it to GitHub. This is your first portfolio piece.
    

---

### 🧩 Phase 2 — LangChain + RAG system (Weeks 3–4)

- [ ]  **Complete Phase 2**
- **📅 Weeks:** 3–4 — *LangChain v1.x + building your first RAG pipeline*
- **⏱️ Time:** ~2 weeks
- **📚 Learn (check off):**
    - [ ]  **LangChain core concepts — chains, LCEL (pipe operator), output parsers**
        
        LangChain v1.0 (stable since Oct 2025) uses LCEL — the | pipe operator to compose chains. Learn this pattern first before touching agents.
        
    - [ ]  **What embeddings are and why they matter**
        
        Text → vector → similarity search. Understand that OpenAI's text-embedding-3-small or sentence-transformers/MiniLM are used to convert text to numbers you can search.
        
    - [ ]  **Document loaders + text splitters**
        
        Load PDFs, CSVs, websites into LangChain. Chunk them with RecursiveCharacterTextSplitter. Understand why chunk size matters (200–800 tokens, 10–20% overlap).
        
    - [ ]  **Vector databases — ChromaDB (local, free) → Pinecone (cloud)**
        
        Start with ChromaDB (runs locally, zero cost). Later move to Pinecone for cloud. Understand collections, similarity search (cosine distance), and retrieval.
        
    - [ ]  **Build a full RAG chain — ingest → embed → store → retrieve → generate**
        
        This is the most in-demand pattern in enterprise AI in 2026. 57% of organizations run RAG over fine-tuning (LangChain State of AI Agents, 2026).
        
    - [ ]  **LangSmith basics — tracing your chains**
        
        89% of production AI teams use observability. LangSmith is LangChain's free tracing tool. Adding it takes 3 lines. Put it in every project — it shows interviewers you think in production terms.
        
- **🔗 Resources:**
    - [ ]  📗 **LangChain Academy (free)** — academy.langchain.com. Official courses written by the LangChain team. Start here, not random blog posts.
    - [ ]  📗 **DataCamp: RAG with LangChain and FastAPI** — step-by-step production RAG tutorial, current (2025).
    - [ ]  📗 **FreeCodeCamp: Production-Ready RAG with FAISS + FastAPI** — free, practical, includes guardrails.
- **🏷️ Tags:**
    - LangChain v1.x
    - LCEL
    - ChromaDB
    - Pinecone
    - FAISS
    - OpenAI Embeddings
    - LangSmith
- **🛠️ Project: Document Q&A system**
    
    Build a RAG system that lets a user upload a PDF or paste text, indexes it in ChromaDB, and answers questions about it. Add a simple Streamlit frontend. Push to GitHub with a proper README. This is your core portfolio piece.
    

---

### 🧠 Phase 3 — LangGraph + multi-agent systems (Weeks 5–6)

- [ ]  **Complete Phase 3**
- **📅 Weeks:** 5–6 — *LangGraph — building agents that actually reason*
- **⏱️ Time:** ~2 weeks
- ⚠ **Important:** LangGraph is separate from LangChain. LangChain is for linear chains. LangGraph is for agents with loops, branching, and memory. In 2026, LangGraph proficiency is what separates junior from senior AI engineers (verified: JetBrains, LangChain docs).
- **📚 Learn (check off):**
    - [ ]  **LangGraph core concepts — StateGraph, Nodes, Edges, State**
        
        Every LangGraph agent is a directed graph. Nodes are functions. Edges define flow. State is a TypedDict that flows through the whole pipeline. Learn this mental model first.
        
    - [ ]  **Tool definition and tool calling**
        
        Define Python functions as tools (using @tool or Pydantic). The LLM decides which tool to call, LangGraph handles execution. This is the core of every production agent.
        
    - [ ]  **Memory — short-term (conversation) and long-term (persistent)**
        
        LangGraph has MemorySaver (in-memory) and PostgreSQL/Redis checkpointers for production. Understand both.
        
    - [ ]  **Human-in-the-loop with interrupt_before**
        
        Production agents need human approval before irreversible actions. LangGraph's interrupt_before is the standard pattern. This is a real interview topic.
        
    - [ ]  **Multi-agent systems — supervisor pattern**
        
        A supervisor agent delegates to specialized sub-agents. This is the dominant enterprise architecture. Build a 2-agent system (researcher + writer, or planner + executor).
        
    - [ ]  **Agentic RAG — agents that decide when to retrieve**
        
        Combine RAG + LangGraph: the agent retrieves documents as a tool call, not automatically. More flexible, more production-realistic.
        
- **🔗 Resources:**
    - [ ]  📗 **LangChain Academy — Intro to LangGraph** (free, official, flagship course). Start here, not elsewhere.
    - [ ]  📗 **LangGraph docs** — docs.langchain.com/oss/python/langgraph. Read the conceptual guides after finishing Academy.
    - [ ]  📗 **30+ LangChain & LangGraph Projects (free PDF)** — codersarts.com. Structured project list, beginner to advanced, with build times.
- **🏷️ Tags:**
    - LangGraph v1.x
    - StateGraph
    - @tool decorator
    - MemorySaver
    - CrewAI
    - Tavily Search
- **🛠️ Project: Research agent with web search + RAG**
    
    An agent that takes a user question, decides whether to search the web (via Tavily) or query your RAG knowledge base, synthesizes the result, and returns a sourced answer. This is a real enterprise use case and strong portfolio piece.
    

---

### 🚀 Phase 4 — FastAPI deployment (Week 7)

- [ ]  **Complete Phase 4**
- **📅 Week:** 7 — *Wrap your agent in a FastAPI — make it a real service*
- **⏱️ Time:** ~1 week
- **📚 Learn (check off):**
    - [ ]  **FastAPI fundamentals — routes, request/response models, Swagger UI**
        
        FastAPI auto-generates interactive API docs at /docs. This is what you demo to interviewers. Learn POST /query, POST /ingest, GET /health endpoints.
        
    - [ ]  **Async endpoints — async def in FastAPI**
        
        FastAPI + async = handles multiple requests simultaneously. Non-async LLM endpoints block under load. This is a common interview gotcha.
        
    - [ ]  **Streaming responses — streaming LLM output via FastAPI**
        
        Users expect token-by-token streaming (like ChatGPT). Learn StreamingResponse and how to yield LangChain/LangGraph streaming events.
        
    - [ ]  **Environment config and security basics**
        
        API key auth headers, CORS configuration, rate limiting basics. Don't expose raw LLM endpoints without any auth — every interviewer will ask about this.
        
- **🏷️ Tags:**
    - FastAPI
    - Uvicorn
    - Pydantic v2
    - StreamingResponse
    - python-dotenv

---

### ☁️ Phase 5 — Docker + cloud deployment (Week 8)

- [ ]  **Complete Phase 5**
- **📅 Week:** 8 — *Docker + deploy to cloud so it's live on the internet*
- **⏱️ Time:** ~1 week
- **📚 Learn (check off):**
    - [ ]  **Docker fundamentals — Dockerfile, docker build, docker run**
        
        Write a Dockerfile for your FastAPI app. This is in 15% of all AI job postings. If you can containerize your app, you're ahead of most applicants.
        
    - [ ]  **docker-compose for multi-service apps**
        
        Your app + a vector DB (Qdrant, Chroma) + Redis = multiple services. docker-compose.yml wires them together. This is how production systems are structured locally.
        
    - [ ]  **Deploy to a free cloud platform (Render, Railway, or Fly.io)**
        
        Don't just run it locally. Deploy it so it has a real URL. Render and Railway offer free tiers that can run a FastAPI + agent app. This is your live demo link for applications.
        
    - [ ]  **Basic GitHub Actions CI/CD**
        
        Auto-deploy on git push. 5-line YAML file. Every serious job posting mentions CI/CD — knowing the concept is enough at this stage.
        
- **🏷️ Tags:**
    - Docker
    - docker-compose
    - Render / Railway
    - GitHub Actions
- 💡 After Week 8, you have a live, deployed agentic AI app with a real URL. That puts you ahead of 80% of applicants who only have Jupyter notebooks.

---

### 🏁 Phase 6 — Capstone project (Weeks 9–10)

- [ ]  **Complete Phase 6**
- **📅 Weeks:** 9–10 — *One production-grade project that shows everything*
- **⏱️ Time:** ~2 weeks
- Pick ONE of these. Don't try to build all of them. Finish, deploy, and document one properly.
- **🎯 Capstone (pick ONE option):**
    - [ ]  **Option A — AI research assistant (recommended)**
        
        Multi-agent system: supervisor routes to a web-search agent + RAG agent. FastAPI backend. Streamlit or Next.js frontend. Deployed live. LangSmith tracing visible. Shows: multi-agent, RAG, tool calling, deployment, observability.
        
    - [ ]  **Option B — Agentic document processor**
        
        Upload any document (PDF, CSV). Agent extracts key info, answers questions, generates summaries, and creates a structured report. Shows: RAG, LangGraph, FastAPI, file handling, production guardrails.
        
    - [ ]  **Option C — AI workflow automation bot**
        
        Agent that takes a task description, breaks it into subtasks, executes them using real APIs (e.g., send email, search web, create a calendar event via n8n). Shows: planning, tool use, real-world integration.
        
- **✅ Your capstone must have:**
    - [ ]  GitHub repo with clean README + architecture diagram
    - [ ]  Live URL
    - [ ]  LangSmith or observability tracing
    - [ ]  A demo video (2 min max, posted on LinkedIn)

---

## Learning log (optional)

Use this section for day-by-day notes.

### Entries

- **Date:**
    
    **What I studied:**  
    
    **Key takeaways:**  
    
    **Next:**