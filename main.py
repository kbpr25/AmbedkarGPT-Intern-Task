import os
import sys
import warnings

# Suppress standard warnings
warnings.filterwarnings("ignore")

# --- IMPORTS ---
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter 
from langchain_huggingface import HuggingFaceEmbeddings

# FIXED: Use the new dedicated library for Ollama (Removes Deprecation Warning)
from langchain_ollama import OllamaLLM

# Using SKLearnVectorStore (Compatible with Python 3.14)
from langchain_community.vectorstores import SKLearnVectorStore

def main():
    print("--- AmbedkarGPT Initialization ---")
    
    # 1. Load the provided text file
    if not os.path.exists("speech.txt"):
        print("Error: speech.txt not found! Please create it first.")
        return
        
    print("1. Loading text...")
    try:
        loader = TextLoader("speech.txt", encoding="utf-8")
        documents = loader.load()
    except Exception as e:
        print(f"Error loading file: {e}")
        return

    # 2. Split the text 
    print("2. Splitting text...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    texts = text_splitter.split_documents(documents)
    
    num_chunks = len(texts)
    print(f"   Split into {num_chunks} chunks.")

    # 3. Create Embeddings
    print("3. Initializing Embeddings (HuggingFace)...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # 4. Create Vector Store (Scikit-Learn)
    print("4. Creating Vector Store (SKLearn)...")
    vectorstore = SKLearnVectorStore.from_documents(
        documents=texts, 
        embedding=embeddings,
        serializer="json" 
    )
    
    # Dynamically set k based on document size
    safe_k = min(num_chunks, 4)
    retriever = vectorstore.as_retriever(search_kwargs={"k": safe_k})

    # 5. Initialize LLM (Ollama)
    print("5. Connecting to Ollama (Llama 3.2)...")
    
    # FIXED: Using OllamaLLM from the new package
    llm = OllamaLLM(model="llama3.2:1b")

    print("\n--- System Ready! Ask questions about the speech. (Type 'exit' to quit) ---")

    while True:
        try:
            query = input("\nYour Question: ")
            if query.lower() in ['exit', 'quit', 'q']:
                print("Exiting...")
                break
            
            print("   Thinking...")
            
            # --- MANUAL RAG PIPELINE ---
            
            # Step A: Retrieve relevant docs
            retrieved_docs = retriever.invoke(query)
            
            # Step B: Combine context
            context_text = "\n\n".join([doc.page_content for doc in retrieved_docs])
            
            if not context_text.strip():
                 print("Error: No context found. Is speech.txt empty?")
                 continue

            # Step C: Create a prompt (Historical Context Safety Wrapper)
            prompt = f"""You are an educational assistant analyzing a historical speech by Dr. B.R. Ambedkar.
            Answer the user's question strictly based on the provided text excerpt.
            
            Context (Historical Text):
            {context_text}

            Question: 
            {query}

            Answer:"""

            # Step D: Get answer from LLM
            response = llm.invoke(prompt)
            
            print(f"\nAnswer: {response}")
            
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()