"""
PersistentId model for unification validation.
"""

from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, model_validator

from .utils import validate_sql_symbol


class PersistentId(BaseModel):
    """
    Defines persistent ID configuration for unification.
    """
    name: str = Field(min_length=1)
    merge_by_persistent_ids: List[str] = Field(default_factory=list, max_length=64)
    merge_by_keys: List[str] = Field(default_factory=list, max_length=64)
    source_tables: Optional[List[str]] = None
    merge_iterations: int = Field(default=3, gt=0, lt=50)
    incremental_merge_iterations: int = Field(default=2, gt=0, lt=50)

    @field_validator('name')
    @classmethod
    def validate_name_sql_symbol(cls, v):
        return validate_sql_symbol(v)

    @model_validator(mode='after')
    def validate_merge_requirements(self):
        """Validate merge requirements"""
        if len(self.merge_by_persistent_ids) <= 1 and len(self.merge_by_keys) == 0:
            raise ValueError("must have at least one merge_by_keys element if merge_by_persistent_ids is 0 or 1")
        return self

    @model_validator(mode='after')
    def validate_time_constraints(self):
        """Validate 'time' key constraints"""
        time_count = self.merge_by_keys.count('time') if self.merge_by_keys else 0
        
        if time_count == 1:
            if self.merge_by_persistent_ids:
                raise ValueError('"time" cannot be specified with merge_by_persistent_ids option')
        elif time_count > 1:
            raise ValueError('too many "time" entries in merge_by_keys')
        
        return self

    model_config = {"extra": "forbid"}