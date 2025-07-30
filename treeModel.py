from typing import Dict,List,Any
from property import Entity,Relationship
import networkx as nx
class ContextTree:
    """Hierarchical representation of context with entities and relationships"""

    def __init__(self):
        self.entities: Dict[str, Entity] = {}
        self.relationships: List[Relationship] = []
        self.graph = nx.DiGraph()

    def add_entity(self, entity: Entity):
        """Add an entity to the context tree"""
        self.entities[entity.id] = entity
        self.graph.add_node(entity.id, **entity.__dict__)

    def add_relationship(self, relationship: Relationship):
        """Add a relationship between entities"""
        self.relationships.append(relationship)
        self.graph.add_edge(
            relationship.source_id,
            relationship.target_id,
            relation_type=relationship.relation_type.value,
            confidence=relationship.confidence,
            description=relationship.description
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert context tree to dictionary representation"""
        return {
            "entities": {eid: {
                "name": entity.name,
                "type": entity.entity_type.value,
                "properties": entity.properties,
                "behaviors": entity.behaviors,
                "confidence": entity.confidence
            } for eid, entity in self.entities.items()},
            "relationships": [{
                "source": rel.source_id,
                "target": rel.target_id,
                "type": rel.relation_type.value,
                "confidence": rel.confidence,
                "description": rel.description
            } for rel in self.relationships]
        }
