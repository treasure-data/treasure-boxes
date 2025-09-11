"""
RelationKeyColumn model for unification validation.
"""

from pydantic import BaseModel, Field, field_validator

from .utils import validate_sql_symbol


class RelationKeyColumn(BaseModel):
    """
    Associates relation keys with specific table columns.
    """
    relation_key_name: str
    relation_table_as_name: str
    column: str = Field(min_length=1)

    @field_validator('column')
    @classmethod
    def validate_column_sql_symbol(cls, v):
        return validate_sql_symbol(v)

    model_config = {"extra": "forbid"}