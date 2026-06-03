import os

STRUCTURE = {
    "rag-project": {
        "app": {
            "main.py": "# Entry point of the API (FastAPI / Flask server)\n",
            "routes": {
                "chat.py": "# API route handling chat requests for the RAG system\n"
            },
            "config.py": "# Configuration file for environment variables and settings\n"
        },

        "rag": {
            "ingestion": {
                "loader.py": "# Loads raw data (PDF, TXT, web pages)\n",
                "cleaner.py": "# Cleans raw text (remove noise, normalize text)\n",
                "splitter.py": "# Splits documents into chunks for embeddings\n"
            },

            "embeddings": {
                "embedder.py": "# Wrapper for embedding models (HF, OpenAI, etc.)\n",
                "models.py": "# Handles selection and configuration of embedding models\n"
            },

            "vectorstore": {
                "faiss_store.py": "# FAISS vector database implementation\n",
                "chroma_store.py": "# Optional ChromaDB vector store implementation\n",
                "base.py": "# Abstract base class for vector stores\n"
            },

            "retrieval": {
                "retriever.py": "# Retrieves top-k relevant chunks from vector store\n",
                "reranker.py": "# Optional reranking of retrieved documents\n"
            },

            "generation": {
                "prompt_builder.py": "# Builds prompts for the LLM using retrieved context\n",
                "llm.py": "# Wrapper around LLMs (Mistral, GPT, etc.)\n"
            },

            "pipeline.py": "# Orchestrates full RAG pipeline (retrieve -> generate)\n"
        },

        "data": {
            "raw": {},
            "processed": {},
            "indexes": {}
        },

        "tests": {
            "test_ingestion.py": "# Tests for ingestion pipeline\n",
            "test_retrieval.py": "# Tests for retrieval system\n",
            "test_pipeline.py": "# Tests full RAG pipeline\n"
        },

        "scripts": {
            "build_index.py": "# Script to build vector index from documents\n",
            "query_test.py": "# CLI tool to test RAG queries\n"
        },

        "requirements.txt": "# Python dependencies for the project\n",
        ".env": "# Environment variables (API keys, configs)\n",
        "README.md": "# Project documentation\n"
    }
}


def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)

        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            # create file with comment
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)


if __name__ == "__main__":
    root = os.getcwd()
    create_structure(root, STRUCTURE)
    print("RAG project structure created successfully.")