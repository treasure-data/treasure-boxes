"""
RelationKey model for unification validation.
"""

from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

from .utils import validate_sql_symbol


class RelationKey(BaseModel):
    """
    Validates relation keys used in unification configuration.
    """
    name: str = Field(min_length=1)
    valid_regexp: Optional[str] = Field(None, min_length=1, max_length=512)
    invalid_texts: Optional[List[Optional[str]]] = None

    @field_validator('name')
    @classmethod
    def validate_name_sql_symbol(cls, v):
        return validate_sql_symbol(v)

    @field_validator('invalid_texts', mode='before')
    @classmethod
    def normalize_empty_arrays(cls, v):
        """Convert empty arrays to None"""
        if v is not None and len(v) == 0:
            return None
        return v

    @field_validator('invalid_texts')
    @classmethod
    def validate_invalid_texts_length(cls, v):
        if v is not None and len(v) > 127:
            raise ValueError("invalid_texts cannot have more than 127 elements")
        return v

    model_config = {"extra": "forbid"}