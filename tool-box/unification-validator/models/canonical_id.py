"""
CanonicalId model for unification validation.
"""

from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, model_validator

from .utils import validate_sql_symbol


class CanonicalId(BaseModel):
    """
    Defines canonical ID configuration for unification.
    """
    name: str = Field(min_length=1)
    do_not_merge_key: Optional[str] = Field(None, min_length=1, max_length=64)
    merge_by_canonical_ids: List[str] = Field(default_factory=list, max_length=64)
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
        if len(self.merge_by_canonical_ids) <= 1 and len(self.merge_by_keys) == 0:
            raise ValueError("must have at least one merge_by_keys element if merge_by_canonical_ids is 0 or 1")
        return self

    @model_validator(mode='after') 
    def validate_do_not_merge_key_applicability(self):
        """Validate do_not_merge_key requirements"""
        if self.do_not_merge_key and self.merge_by_keys:
            if self.merge_by_keys[0] != self.do_not_merge_key:
                first_key = self.merge_by_keys[0]
                raise ValueError(f"do_not_merge_key must be first element of merge_by_keys which is '{first_key}' but '{self.do_not_merge_key}' is used")
        return self

    model_config = {"extra": "forbid"}