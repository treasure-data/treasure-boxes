"""
Unification Validator: Python package for validating ID Unification YAML files.

This package provides Pydantic models and validation logic for local validation 
of unification configuration files.
"""

__version__ = "1.0.0"

from models import (
    RelationKey,
    RelationKeyColumn,
    RelationTable,
    CanonicalId,
    PersistentId,
    MasterTable,
    MasterTableAttribute,
    MasterTableAttributeSourceColumn,
    Unification,
)
from yaml_loader import load_unification_yaml
from cli import validate_yaml_file

__all__ = [
    "RelationKey",
    "RelationKeyColumn", 
    "RelationTable",
    "CanonicalId",
    "PersistentId",
    "MasterTable",
    "MasterTableAttribute",
    "MasterTableAttributeSourceColumn",
    "Unification",
    "load_unification_yaml",
    "validate_yaml_file",
]