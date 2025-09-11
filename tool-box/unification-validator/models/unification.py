"""
UnificationRevision model for unification validation.
"""

from typing import List
from pydantic import BaseModel, Field, field_validator, model_validator

from .utils import validate_sql_symbol
from .relation_key import RelationKey
from .relation_table import RelationTable
from .canonical_id import CanonicalId
from .persistent_id import PersistentId
from .master_table import MasterTable


class Unification(BaseModel):
    """
    Top-level container for unification configuration.
    """
    name: str = Field(min_length=1)
    keys: List[RelationKey] = Field(min_length=1)
    tables: List[RelationTable] = Field(min_length=1)
    canonical_ids: List[CanonicalId] = Field(default_factory=list)
    persistent_ids: List[PersistentId] = Field(default_factory=list)
    master_tables: List[MasterTable] = Field(default_factory=list)

    @field_validator('name')
    @classmethod
    def validate_name_sql_symbol(cls, v):
        return validate_sql_symbol(v)

    @model_validator(mode='after')
    def validate_either_canonical_or_persistent_ids(self):
        """Ensure either canonical_ids or persistent_ids has at least one item"""
        if len(self.canonical_ids) == 0 and len(self.persistent_ids) == 0:
            raise ValueError("either canonical_ids or persistent_ids must have at least one item")
        return self

    @model_validator(mode='after')
    def validate_cross_references(self):
        """Validate cross-references between models"""
        # Note: Most cross-reference validation is now handled by collect_additional_errors
        # in cli.py to provide better error formatting and location information.
        # This validator is kept minimal to avoid duplicate error messages.
        return self

    model_config = {
        "extra": "forbid",
        "validate_assignment": True,
        "validate_default": True
    }