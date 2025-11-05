"""
MasterTableAttributeSourceColumn model for unification validation.
"""

from typing import Optional
from pydantic import BaseModel, Field, field_validator

from .utils import validate_sql_symbol


class MasterTableAttributeSourceColumn(BaseModel):
    """
    Defines source column specifications for master table attributes.
    """
    relation_table_as_name: str
    column: str = Field(min_length=1)
    priority: Optional[int] = Field(None, ge=1)
    order_type: Optional[str] = None

    @field_validator('column')
    @classmethod
    def validate_column_sql_symbol(cls, v):
        return validate_sql_symbol(v)

    model_config = {"extra": "forbid"}