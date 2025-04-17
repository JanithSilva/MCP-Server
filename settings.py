import os
from dotenv import load_dotenv
from typing import Dict, Any

def load_config() -> Dict[str, Any]:
    load_dotenv()
    return {
        "sharepoint": {
            "url": os.getenv("SHAREPOINT_SITE_URL"),
            "username": os.getenv("SHAREPOINT_USERNAME"),
            "password": os.getenv("SHAREPOINT_PASSWORD"),
            "library_name": os.getenv("SHAREPOINT_LIBRARY_NAME"),
        },
        "neo4j": {
            "uri": os.getenv("NEO4J_URI"),
            "user": os.getenv("NEO4J_USER"),
            "password": os.getenv("NEO4J_PASSWORD")
        },
        "openai-embedding": {
            "azure_endpoint": os.getenv("EMBEDDING_MODEL_ENDPOINT"),
            "api_key": os.getenv("EMBEDDING_MODEL_KEY"),
            "api_version": os.getenv("EMBEDDING_MODEL_API_VERSION"),
            "deployment": os.getenv("EMBEDDING_MODEL_DEPLOYMENT_NAME"),
            "chunk_size": int(os.getenv("EMBEDDING_MODEL_CHUNK_SIZE")),
            "dimension": int(os.getenv("EMBEDDING_MODEL_DIMENSION")),
            "chunk_overlap": int(os.getenv("EMBEDDING_MODEL_CHUNK_OVERLAP")),
        },
        "openai-llm": {
            "api_version": os.getenv("LLM_API_VERSION"),
            "azure_deployment": os.getenv("LLM_DEPLOYMENT_NAME"),
            "api_key": os.getenv("LLM_API_KEY"),
            "azure_endpoint": os.getenv("LLM_API_ENDPOINT"),
        }
    }