"""
MasterTableAttribute model for unification validation.
"""

from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, model_validator

from .utils import validate_sql_symbol
from .master_table_attribute_source_column import MasterTableAttributeSourceColumn


class MasterTableAttribute(BaseModel):
    """
    Defines attributes for master tables.
    """
    name: str = Field(min_length=1)
    array_elements: Optional[int] = Field(None, ge=1, le=10)
    source_canonical_id: Optional[str] = None
    source_persistent_id: Optional[str] = None
    valid_regexp: Optional[str] = Field(None, min_length=1, max_length=512)
    invalid_texts: Optional[List[Optional[str]]] = None
    source_columns: List[MasterTableAttributeSourceColumn] = Field(default_factory=list)

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

    @model_validator(mode='after')
    def validate_source_requirements(self):
        """Validate source requirements for table attributes"""
        # If we have a canonical or persistent ID, validate source column requirements
        if self.source_canonical_id is not None and len(self.source_columns) > 0:
            raise ValueError("source_columns must not be set when source_canonical_id is set")
        elif self.source_canonical_id is None and len(self.source_columns) == 0:
            # Only require source_columns if we don't have source_canonical_id or source_persistent_id
            if self.source_persistent_id is None:
                raise ValueError("source_columns must be set when neither source_canonical_id nor source_persistent_id is set")
        
        if self.source_persistent_id is not None and len(self.source_columns) > 0:
            raise ValueError("source_columns must not be set when source_persistent_id is set")
        elif self.source_persistent_id is None and len(self.source_columns) == 0:
            # Only require source_columns if we don't have source_persistent_id or source_canonical_id  
            if self.source_canonical_id is None:
                raise ValueError("source_columns must be set when neither source_persistent_id nor source_canonical_id is set")
        
        return self

    model_config = {"extra": "forbid"}