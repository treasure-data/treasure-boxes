"""
RelationTable model for unification validation.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator

from .utils import validate_sql_symbol


class RelationTable(BaseModel):
    """
    Defines source tables for unification.
    """
    database_name: str = Field(min_length=1)
    table_name: str = Field(min_length=1)
    as_name: str = Field(min_length=1)
    incremental_columns: Optional[List[str]] = None
    key_columns: List[Dict[str, Any]] = Field(min_length=1, max_length=32)

    @field_validator('database_name')
    @classmethod
    def validate_database_name_sql_symbol(cls, v):
        return validate_sql_symbol(v)

    @field_validator('table_name')
    @classmethod
    def validate_table_name_sql_symbol(cls, v):
        return validate_sql_symbol(v)

    @field_validator('as_name')
    @classmethod
    def validate_as_name_sql_symbol(cls, v):
        return validate_sql_symbol(v)

    @field_validator('incremental_columns', mode='before')
    @classmethod
    def normalize_incremental_columns(cls, v):
        """Convert empty arrays to None"""
        if v is not None and len(v) == 0:
            return None
        return v

    @field_validator('incremental_columns')
    @classmethod
    def validate_incremental_columns_length(cls, v):
        if v is not None and len(v) > 127:
            raise ValueError("incremental_columns cannot have more than 127 elements")
        return v

    model_config = {"extra": "forbid"}