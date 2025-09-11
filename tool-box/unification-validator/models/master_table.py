"""
MasterTable model for unification validation.
"""

from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, model_validator

from .utils import validate_sql_symbol
from .master_table_attribute import MasterTableAttribute


class MasterTable(BaseModel):
    """
    Defines master tables for unification output.
    """
    name: str = Field(min_length=1)
    canonical_id: Optional[str] = None
    persistent_id: Optional[str] = None
    attributes: List[MasterTableAttribute] = Field(default_factory=list, max_length=512)

    @field_validator('name')
    @classmethod
    def validate_name_sql_symbol(cls, v):
        return validate_sql_symbol(v)

    @model_validator(mode='after')
    def validate_having_either_canonical_id_or_persistent_id(self):
        """Validate that either canonical_id or persistent_id is present"""
        # XOR: exactly one must be present
        if not (bool(self.canonical_id) ^ bool(self.persistent_id)):
            raise ValueError('either canonical_id or persistent_id must be present (but not both)')
        return self

    @model_validator(mode='after')
    def validate_unique_attribute_names(self):
        """Ensure attribute names are unique within the master table"""
        attribute_names = [attr.name for attr in self.attributes]
        seen_names = set()
        
        for name in attribute_names:
            if name in seen_names:
                raise ValueError(f'duplicate attribute name "{name}"')
            seen_names.add(name)
        
        return self

    model_config = {"extra": "forbid"}