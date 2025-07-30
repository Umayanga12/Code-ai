from enum import Enum
from dataclasses import dataclass
from typing import List
class EntityType(Enum):
    PERSON = "person"
    OBJECT = "object"
    CONCEPT = "concept"
    ACTION = "action"
    LOCATION = "location"
    TIME = "time"
    ATTRIBUTE = "attribute"

class RelationType(Enum):
    HAS_PROPERTY = "has_property"
    PERFORMS_ACTION = "performs_action"
    LOCATED_AT = "located_at"
    RELATED_TO = "related_to"
    CONTAINS = "contains"
    CAUSES = "causes"
    DEPENDS_ON = "depends_on"

@dataclass
class Entity:
    """Represents an entity in the context tree"""
    id: str
    name: str
    entity_type: EntityType
    properties: List[str] = None
    behaviors: List[str] = None
    confidence: float = 0.0

    def __post_init__(self):
        if self.properties is None:
            self.properties = []
        if self.behaviors is None:
            self.behaviors = []

@dataclass
class Relationship:
    """Represents a relationship between entities"""
    source_id: str
    target_id: str
    relation_type: RelationType
    confidence: float = 0.0
    description: str = ""
