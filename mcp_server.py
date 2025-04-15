# math_server.py
from mcp.server.fastmcp import FastMCP
from services.graph_store import GraphStoreService
from services.sharepoint import SharePointService
from settings import load_config
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


config = load_config()
graph_service = GraphStoreService()
sharepoint_service = SharePointService(config["sharepoint"])

mcp = FastMCP("Tools")


@mcp.tool(
    name="metadata_retrieve",
    description="Returns structured metadata from the SharePoint 'Documents' library for use in LLM context."
)
async def metadata_retrieve() -> str:
    """
    Retrieve and return structured metadata from SharePoint files as a string.

    Args:
        query (str): A keyword or phrase to filter metadata (e.g., filename, author, title).

    Returns:
        str: A structured string (JSON Lines).
    """
    metadata = sharepoint_service.get_metadata()
   
    return metadata



@mcp.tool(
    name="entity_retrieve",
    description="Query the knowledge graph using semantic similarity to find relevant entities and their relationships."
)
async def entity_retrieve(query: str) -> str:
    """
    Retrieves relevant entities from the Neo4j knowledge graph based on semantic similarity to the input query.

    Args:
        query (str): The natural language search query for entities.

    Returns:
        List[str]: A list of entity descriptions formatted for user understanding.
    """
   

    entities = graph_service.query_semantically(question = query, top_k=5, score_threshold=0.75)
   
    return entities


if __name__ == "__main__":
    mcp.run(transport="sse")