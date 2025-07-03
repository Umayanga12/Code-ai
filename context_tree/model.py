from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class Property:
    name: str
    type: str
    constraints: List[str] = field(default_factory=list)

@dataclass
class Entity:
    name: str
    properties: Dict[str, Property] = field(default_factory=dict)
    actions: List[str] = field(default_factory=list)

@dataclass
class Relationship:
    from_entity: str
    to_entity: str
    relation_type: str

@dataclass
class MLTask:
    name: str
    input_fields: List[str]
    output_fields: List[str]
    model_type: str

@dataclass
class ProjectContext:
    entities: Dict[str, Entity] = field(default_factory=dict)
    relationships: List[Relationship] = field(default_factory=list)
    ml_tasks: List[MLTask] = field(default_factory=list)
    config: Dict[str, str] = field(default_factory=dict)
