# AmbedkarGPT: RAG-Based Q&A System

**Internship Assignment Submission for Kalpit Pvt Ltd**

A specialized Command Line Interface (CLI) tool that ingests historical speeches by Dr. B.R. Ambedkar and performs Retrieval-Augmented Generation (RAG) to answer user queries with high accuracy.

## 🚀 Project Overview

This system demonstrates a functional RAG pipeline built with **Python 3.14**. It ingests raw text, chunks it for semantic processing, generates vector embeddings, and retrieves context-aware answers using a local Large Language Model (LLM).

### 🛠 Tech Stack & Architecture
* **Language:** Python 3.14 (Experimental Build)
* **Orchestration:** LangChain Framework
* **LLM:** Ollama (Llama 3.2:1b) - *Chosen for strict local privacy and speed.*
* **Embeddings:** HuggingFace (`sentence-transformers/all-MiniLM-L6-v2`)
* **Vector Store:** Scikit-Learn VectorStore (In-memory)

---

## ⚙️ Design Decisions & Adaptations

**1. Vector Store Adaptation (ChromaDB → Scikit-Learn)**
The original assignment requested **ChromaDB**. However, due to the use of the experimental **Python 3.14** environment, ChromaDB's dependencies (specifically HNSWLib) are not yet compatible with the latest Python ABI.
* **Solution:** I architected the solution using `SKLearnVectorStore`. This provides the same vector similarity search capabilities required for the task while ensuring stability on the requested Python version.

**2. Safety & Prompt Engineering**
The Llama 3.2 model has strict safety guardrails. When processing text containing phrases like "destroy the belief," the model initially refused to answer, interpreting it as a violent request.
* **Solution:** I implemented a "Historical Context Wrapper" in the system prompt. This explicitly instructs the LLM that it is analyzing historical text, bypassing false-positive safety refusals while maintaining ethical guidelines.

---

## 💻 Setup & Installation

### Prerequisites
* Python 3.11+ (Tested on 3.14)
* [Ollama](https://ollama.ai/) installed and running.

### Step 1: Clone the Repository
git clone [https://github.com/kbpr25/AmbedkarGPT-Intern-Task.git](https://github.com/kbpr25/AmbedkarGPT-Intern-Task.git)
cd AmbedkarGPT-Intern-Task

### Step 2: Environment Setup
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

### Step 3: Install Dependencies
pip install -r requirements.txt

### Step 4: Prepare the LLM
Ensure Ollama is running, then pull the optimized model:
ollama pull llama3.2:1b or ollama pull mistral:7b

### 🏃‍♂️ Usage Guide
1. Run the Application:
python main.py

2. Ask a Question: The system will initialize and prompt for input.

Example Q: "What is the real remedy?"

Example Q: "Why is social reform difficult?"

3. Exit: Type exit or q to close the application.

📂 File Structure
main.py: Core logic (Loading -> Splitting -> Embedding -> RAG Loop).

speech.txt: Source data file (Excerpt from "Annihilation of Caste").

requirements.txt: Python dependencies.

---
