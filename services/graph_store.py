import json
from langchain_neo4j import Neo4jGraph
from langchain_openai import AzureOpenAIEmbeddings
from settings import load_config

class GraphStoreService:
    def __init__(self):
        config = load_config()

        neo4j_config = config["neo4j"]
        self.neo4j_graph = Neo4jGraph(
            url=neo4j_config["uri"],
            username=neo4j_config["user"],
            password=neo4j_config["password"]
        )
        
        embedding_config = config["openai-embedding"]
        self.embeddings = AzureOpenAIEmbeddings(
            azure_deployment=embedding_config["deployment"],
            openai_api_version=embedding_config["api_version"],
            azure_endpoint=embedding_config["azure_endpoint"],
            api_key=embedding_config["api_key"],
            chunk_size=embedding_config["chunk_size"]
        )

    def query_semantically(self, question: str, top_k: int = 5, score_threshold: float = 0.75) -> str:
        """
        Query the knowledge graph using semantic similarity to find relevant entities and their relationships.
        
        Args:
            question: The natural language question to query with
            top_k: Number of most similar chunks to return
            score_threshold: Minimum similarity score to include results
            
        Returns:
            List of dictionaries containing relevant entities, their relationships, and connected nodes
        """
       
        #Embed the question
        question_embedding = self.embeddings.embed_query(question)
        
        #Query the vector index for similar chunks
        vector_query = """
        CALL db.index.vector.queryNodes(
            'document_embeddings', 
            $top_k, 
            $question_embedding
        ) YIELD node, score
        WHERE score >= $score_threshold
        RETURN node, score
        ORDER BY score DESC
        """
        vector_results = self.neo4j_graph.query(
            vector_query,
            params={
                "top_k": top_k,
                "question_embedding": question_embedding,
                "score_threshold": score_threshold
            }
        )
    
        if not vector_results:
            return "No relevant entities found."
        
        # Get related entities and their relationships for each matching chunk
        results = []
        for record in vector_results:
            chunk_node = record["node"]
            
            entity_query = """
                MATCH (chunk:Document {id: $chunk_id})
                OPTIONAL MATCH (chunk)-[r1]-(entity)
                WHERE NOT entity:Document  // Exclude other document chunks
                // Now find all relationships for these entities
                OPTIONAL MATCH (entity)-[r2]-(related_node)
                WHERE NOT related_node:Document AND id(entity) < id(related_node)  // This ensures each relationship is only returned once
                RETURN 
                    entity, 
                    labels(entity) as entity_labels, 
                    collect(DISTINCT {
                        relationship: r2,
                        type: type(r2),
                        direction: CASE WHEN startNode(r2) = entity THEN 'FORWARD' ELSE 'BACKWARD' END,
                        related_node: related_node,
                        related_node_labels: labels(related_node)
                    }) as entity_relationships
                """
            entities = self.neo4j_graph.query(
                entity_query,
                params={"chunk_id": chunk_node["id"]}
            )
            results.append(entities)
   
        
        relationships = set()  
        
        for entity_data in results:
            if not entity_data:
                continue
                
            for entity_entry in entity_data:
                if not isinstance(entity_entry, dict):
                    continue
                    
                entity = entity_entry.get('entity', {}).get('id', 'Unknown')
                rels = entity_entry.get('entity_relationships', [])
                
                for rel in rels:
                    if not rel["relationship"]:
                        continue
                        
                    related_node = rel.get('related_node', {}).get('id', 'Unknown')
                    rel_type = rel.get('type', 'UNKNOWN')
                    
                    # Create normalized relationship representation (direction-agnostic)
                    sorted_nodes = sorted([entity, related_node])
                    relationship_key = f"{sorted_nodes[0]}||{rel_type}||{sorted_nodes[1]}"
                    
                    relationships.add(relationship_key)
        
        # Convert to clean output format
        formatted_rels = []
        for rel in relationships:
            source, rel_type, target = rel.split("||")
            formatted_rels.append(f"{source} - {rel_type} -> {target}")
        
        return "\n".join(formatted_rels) if formatted_rels else "No relationships found"