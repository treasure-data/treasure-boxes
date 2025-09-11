# Unification Validator

A Python tool for validating ID Unification YAML files using Pydantic models.

## Purpose

This validator allows users to locally validate their unification YAML files before deployment.

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Usage

### Command Line

```bash
# Validate a single file
python validate.py unification.yml

# Validate multiple files  
python validate.py *.yml
```

## Features

- **Complete validation**: Comprehensive validation logic
- **Field-level validation**: SQL symbols, regex patterns, length limits, etc.
- **Cross-model validation**: References between models, inheritance checks
- **Enhanced error messages**: Shows item names along with array indices for easy identification
- **Comprehensive validation**: Complete field-level and cross-model validation

## Validation Rules

### SQL Symbol Validation
All names must be valid SQL identifiers:
- Start with letter or underscore
- Contain only letters, numbers, and underscores
- Applied to: key names, table names, column names, etc.

### Invalid Texts Support
Both `RelationKey` and `MasterTableAttribute` support `invalid_texts` arrays:
- Can contain string values to exclude from matching
- Supports `null` values within the array
- Empty arrays are normalized to `null`
- Maximum 127 elements per array

### Cross-Reference Validation
- All keys defined in `keys` section must be used in at least one table's `key_columns`
- CanonicalId `merge_by_keys` must reference keys defined in root `keys` section
- PersistentId `merge_by_keys` must reference defined keys (or 'time')
- Table `key_columns` must reference defined keys
- CanonicalId `merge_by_canonical_ids` must reference existing canonical IDs
- MasterTable `canonical_id`/`persistent_id` must exist
- MasterTableAttribute `source_columns` can reference any table name (not restricted to tables section)
- Clear error messages when references are invalid

### Required Root Objects
- `name`: Unification configuration name (SQL symbol)
- `keys`: At least one RelationKey must be defined
- `tables`: At least one RelationTable must be defined
- Either `canonical_ids` OR `persistent_ids`: At least one must have content (but not necessarily both)
- `master_tables`: Optional (can be empty)

### Business Logic Validation
- CanonicalId/PersistentId must have merge keys if inheritance ≤ 1
- MasterTable must have exactly one of canonical_id OR persistent_id
- MasterTable attribute names must be unique within each table
- MasterTableAttribute source requirements based on parent table type

## Model Structure

The validator includes Python Pydantic models converted from:

### Core Models
- **RelationKey**: Defines merge keys with validation patterns
- **RelationTable**: Source data tables with key column mappings  
- **CanonicalId**: Canonical ID unification configuration
- **PersistentId**: Persistent ID unification configuration
- **MasterTable**: Output table definitions
- **MasterTableAttribute**: Column definitions for master tables

### Helper Models
- **RelationKeyColumn**: Key-to-column mappings
- **MasterTableAttributeSourceColumn**: Source column specifications
- **Unification**: Top-level configuration container


## Development

The models implement comprehensive validation logic. Key concepts:

- Field validation using Pydantic validators
- Model-level validation with custom logic  
- Field constraints and length limits
- Cross-model reference validation

Each model is in its own file for better organization and maintainability. The models can be imported individually or through the main package.