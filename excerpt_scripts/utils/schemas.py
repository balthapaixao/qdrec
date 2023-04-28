import pendulum
from dataclasses import dataclass


@dataclass
class ExcerptMetadataSchema:
    """Schema for the metadata excerpt table"""
    excerpt_id: int
    uf: str
    cidade: str
    tema: str
    data_trecho: pendulum.datetime


@dataclass
class NamedEntitySchema:
    """Schema for the named entity table"""
    excerpt_id: int
    content: str
    entity_type: str
    start_offset: int
    end_offset: int


@dataclass
class ExcerptVectorsSchema:
    excerpt_id: int
    vectorized_excerpt: str
