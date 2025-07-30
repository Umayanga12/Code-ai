import spacy
from transformers import pipeline
import re
import logging
from property import Entity, Relationship
from typing import List
from property import EntityType
from property import RelationType
from treeModel import ContextTree

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContextTreeGenerator:
    """Main class for generating context trees from user prompts"""

    def __init__(self):
        # Load spaCy model for NLP processing
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            logger.error("spaCy model not found. Run: python -m spacy download en_core_web_sm")
            raise

        # Load sentence transformer for semantic similarity
        self.sentence_transformer = pipeline(
            "feature-extraction",
            model="sentence-transformers/all-MiniLM-L6-v2",
            return_tensors="pt",
            device=-1
        )

        # Entity type mapping based on spaCy labels
        self.entity_type_mapping = {
            "PERSON": EntityType.PERSON,
            "ORG": EntityType.OBJECT,
            "GPE": EntityType.LOCATION,
            "LOC": EntityType.LOCATION,
            "DATE": EntityType.TIME,
            "TIME": EntityType.TIME,
            "MONEY": EntityType.ATTRIBUTE,
            "QUANTITY": EntityType.ATTRIBUTE,
            "ORDINAL": EntityType.ATTRIBUTE,
            "CARDINAL": EntityType.ATTRIBUTE
        }

        # Behavior keywords
        self.behavior_patterns = [
            r'\b(can|could|will|would|should|might|may)\s+(\w+)',
            r'\b(\w+ing)\b',  # gerunds
            r'\b(able\s+to|capable\s+of)\s+(\w+)',
        ]

    def extract_entities(self, text: str) -> List[Entity]:
        """Extract entities from text using spaCy NER"""
        doc = self.nlp(text)
        entities = []
        entity_counter = {}

        # Extract named entities
        for ent in doc.ents:
            entity_type = self.entity_type_mapping.get(ent.label_, EntityType.CONCEPT)
            entity_id = f"{entity_type.value}_{ent.text.lower().replace(' ', '_')}"

            # Handle duplicate entities
            if entity_id in entity_counter:
                entity_counter[entity_id] += 1
                entity_id = f"{entity_id}_{entity_counter[entity_id]}"
            else:
                entity_counter[entity_id] = 0

            entity = Entity(
                id=entity_id,
                name=ent.text,
                entity_type=entity_type,
                confidence=0.8  # Base confidence for NER
            )
            entities.append(entity)

        # Extract noun phrases as potential entities
        for chunk in doc.noun_chunks:
            if chunk.text not in [ent.name for ent in entities]:
                entity_id = f"concept_{chunk.text.lower().replace(' ', '_')}"
                if entity_id in entity_counter:
                    entity_counter[entity_id] += 1
                    entity_id = f"{entity_id}_{entity_counter[entity_id]}"
                else:
                    entity_counter[entity_id] = 0

                entity = Entity(
                    id=entity_id,
                    name=chunk.text,
                    entity_type=EntityType.CONCEPT,
                    confidence=0.6  # Lower confidence for noun chunks
                )
                entities.append(entity)

        return entities

    def extract_properties_and_behaviors(self, text: str, entities: List[Entity]) -> None:
        """Extract properties and behaviors for entities"""
        doc = self.nlp(text)

        for entity in entities:
            # Find properties (adjectives near the entity)
            for token in doc:
                if entity.name.lower() in token.sent.text.lower():
                    for child in token.sent:
                        if child.pos_ == "ADJ" and child.dep_ in ["amod", "acomp"]:
                            entity.properties.append(child.text)

            # Find behaviors using pattern matching
            for pattern in self.behavior_patterns:
                matches = re.finditer(pattern, text.lower())
                for match in matches:
                    if entity.name.lower() in match.string[max(0, match.start()-50):match.end()+50]:
                        if len(match.groups()) > 1:
                            entity.behaviors.append(match.group(2))
                        else:
                            entity.behaviors.append(match.group(1))

    def extract_relationships(self, text: str, entities: List[Entity]) -> List[Relationship]:
        """Extract relationships between entities"""
        doc = self.nlp(text)
        relationships = []

        # Simple dependency-based relationship extraction
        for token in doc:
            if token.dep_ in ["nsubj", "dobj", "pobj"]:
                head = token.head

                # Find entities involved
                subj_entity = None
                obj_entity = None

                for entity in entities:
                    if entity.name.lower() in token.text.lower():
                        obj_entity = entity
                    if entity.name.lower() in head.text.lower():
                        subj_entity = entity

                if subj_entity and obj_entity and subj_entity.id != obj_entity.id:
                    # Determine relationship type based on POS and dependency
                    if head.pos_ == "VERB":
                        rel_type = RelationType.PERFORMS_ACTION
                    elif token.dep_ == "pobj" and head.text.lower() in ["in", "at", "on"]:
                        rel_type = RelationType.LOCATED_AT
                    else:
                        rel_type = RelationType.RELATED_TO

                    relationship = Relationship(
                        source_id=subj_entity.id,
                        target_id=obj_entity.id,
                        relation_type=rel_type,
                        confidence=0.7,
                        description=f"{subj_entity.name} {head.text} {obj_entity.name}"
                    )
                    relationships.append(relationship)

        return relationships

    def generate_context_tree(self, prompt: str) -> ContextTree:
        """Generate a complete context tree from user prompt"""
        logger.info(f"Processing prompt: {prompt[:100]}...")

        # Initialize context tree
        context_tree = ContextTree()

        # Extract entities
        entities = self.extract_entities(prompt)
        logger.info(f"Extracted {len(entities)} entities")

        # Extract properties and behaviors
        self.extract_properties_and_behaviors(prompt, entities)

        # Add entities to context tree
        for entity in entities:
            context_tree.add_entity(entity)

        # Extract relationships
        relationships = self.extract_relationships(prompt, entities)
        logger.info(f"Extracted {len(relationships)} relationships")

        # Add relationships to context tree
        for relationship in relationships:
            context_tree.add_relationship(relationship)

        return context_tree
