# ASTRA — Agentic Support & Triage Routing Architecture

ASTRA is a multi-agent customer support system built on LangGraph. It uses a state-machine architecture to route customer queries to specialized AI worker nodes, allowing secure interaction with both a relational database (MySQL) and a vector knowledge base (ChromaDB) without hallucination.

## Table of Contents

- [The Problem](#the-problem)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Setup & Installation](#setup--installation)
- [Database Configuration](#database-configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Roadmap](#roadmap)
- [License](#license)

## The Problem

Traditional AI customer support bots tend to fall into one of two traps:

1. **Rigid decision trees** — legacy chatbots force users through menus ("Press 1 for Billing") and fail to understand natural language.
2. **Monolithic LLMs** — giving a single large language model access to all company data and tools at once leads to tool confusion and hallucination. A monolithic agent might search a product manual for a tracking number, or expose sensitive database schemas during a technical support chat.

**The solution:** ASTRA uses a multi-agent state machine that mirrors how a real support department operates:

- A **Classifier Agent** (receptionist) analyzes intent and routes the request.
- A **Technical Specialist Agent**, isolated with access only to a vector database, handles troubleshooting via RAG.
- A **Billing Specialist Agent**, isolated with access only to MySQL, handles real-time order lookups.

This modular design keeps each agent's scope narrow, which makes the system's behavior more secure, deterministic, and accurate.

## Key Features

| Feature | Description |
|---|---|
| **Intent Routing** | Uses Llama 3 (via Groq) to classify user input as `technical`, `billing`, or `general`. |
| **RAG Knowledge Base** | HuggingFace embeddings + ChromaDB for semantic search over manuals and refund policies. |
| **Real-Time SQL Integration** | Direct MySQL queries for live order status, tracking URLs, and delivery dates. |
| **Stateful Memory** | Maintains conversation history across the session. |
| **Fast Inference** | Powered by Groq's LPU inference engine for low-latency responses. |

## Tech Stack

- **Framework:** LangChain & LangGraph
- **LLM Provider:** Groq (Llama 3.3 70B & Llama 3.1 8B)
- **Vector Database:** ChromaDB
- **Embeddings:** HuggingFace (`all-MiniLM-L6-v2`)
- **Relational Database:** MySQL
- **Document Parsing:** Unstructured

## Architecture

```
                        ┌─────────────────────┐
                        │   User Query (CLI)   │
                        └──────────┬───────────┘
                                   ▼
                        ┌─────────────────────┐
                        │   Classifier Agent   │
                        │  (Intent Detection)  │
                        └──────────┬───────────┘
                     ┌─────────────┼─────────────┐
                     ▼             ▼             ▼
             ┌───────────┐ ┌───────────┐ ┌───────────┐
             │ Technical │ │  Billing  │ │  General  │
             │   Agent   │ │   Agent   │ │   Agent   │
             │  (RAG /   │ │  (MySQL)  │ │           │
             │ ChromaDB) │ │           │ │           │
             └───────────┘ └───────────┘ └───────────┘
```

## Prerequisites

- Python 3.9+
- MySQL Server (running locally on port 3306)
- A [Groq API key](https://console.groq.com/)

## Setup & Installation

**1. Clone the repository**

```bash
git clone https://github.com/vanig245/ASTRA
cd ASTRA
```

**2. Create and activate a virtual environment**

```bash
python3 -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install langchain langchain-core langgraph langchain-groq langchain-community langchain-huggingface chromadb unstructured mysql-connector-python python-dotenv
```

**4. Configure environment variables**

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

## Database Configuration

### 1. SQL database (billing / orders)

Ensure MySQL is running, then create the `astra_db` database and an `orders` table with columns for `order_id`, `status`, `estimated_delivery`, and `tracking_url`.

### 2. Vector database (knowledge base)

Place knowledge base text files (e.g., `router.txt`, `hardware_repair.txt`, `refund_policies.txt`) into a `kb_docs/` folder, then run the ingestion script:

```bash
python ingest.py
```

This generates a local `./chroma_db` directory.

## Usage

Start the interactive CLI:

```bash
python graph.py
```

**Example prompts:**

- *Technical route:* "My screen is cracked, how much does it cost to fix?"
- *Billing route:* "Where is my package? My order ID is 010."
- *Follow-up / routing:* "What about water damage?"

## Project Structure

```
ASTRA/
├── memory.py       # Defines the SupportState schema for LangGraph
├── tools.py        # SQL querying (get_order_status) and ChromaDB search (search_kb)
├── nodes.py        # System prompts and LLM tool-bindings for each agent
├── graph.py        # Assembles conditional edges, compiles the graph, runs the CLI
├── ingest.py       # Loads local .txt files into the ChromaDB vector store
└── kb_docs/        # Raw knowledge base text files
```

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.