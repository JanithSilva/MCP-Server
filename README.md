# MCP Server

A Python-based server application that provides tools for metadata retrieval from SharePoint and entity retrieval from a Neo4j knowledge graph using semantic similarity search.

## Features

- **Metadata Retrieval**: Fetches structured metadata from SharePoint's 'Documents' library
- **Entity Retrieval**: Queries a Neo4j knowledge graph using semantic similarity to find relevant entities and their relationships
- **FastMCP Integration**: Built on top of FastMCP framework for tool management and execution

## Prerequisites

- Python 3.x
- Neo4j database
- SharePoint access credentials
- OpenAI API key (for semantic search)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd mcp-server
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
Create a `.env` file with the following variables:
```
SHAREPOINT_URL=
SHAREPOINT_USERNAME=
SHAREPOINT_PASSWORD=
SHAREPOINT_LIBRARY_NAME=

NEO4J_URI=
NEO4J_USER=
NEO4J_PASSWORD=

EMBEDDING_MODEL_ENDPOINT=
EMBEDDING_MODEL_KEY=
EMBEDDING_MODEL_API_VERSION=
EMBEDDING_MODEL_DEPLOYMENT_NAME=
EMBEDDING_MODEL_CHUNK_SIZE=
EMBEDDING_MODEL_DIMENSION=
EMBEDDING_MODEL_CHUNK_OVERLAP=
```

## Usage

1. Start the server:
```bash
python mcp_server.py
```

2. The server provides two main tools:
   - `metadata_retrieve`: Retrieves structured metadata from SharePoint
   - `entity_retrieve`: Queries the knowledge graph using semantic similarity

## Project Structure

```
.
├── mcp_server.py          # Main server application
├── settings.py            # Configuration management
├── services/             # Service implementations
│   ├── graph_store.py    # Neo4j graph operations
│   └── sharepoint.py     # SharePoint integration
├── requirements.txt      # Project dependencies
└── .env                  # Environment variables
```

## Dependencies

- langchain-mcp-adapters
- mcp[cli]
- langchain_openai
- pinecone
- langchain
- langchain_neo4j
- office365-rest-python-client
