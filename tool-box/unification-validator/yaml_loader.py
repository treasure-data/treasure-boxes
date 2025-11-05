"""
YAML loading utilities for unification configuration files.

This module handles loading and preprocessing of unification YAML files
to match the expected structure for validation.
"""

from pathlib import Path
from typing import Dict, Any

import yaml


def load_unification_yaml(file_path: Path) -> Dict[str, Any]:
    """
    Load and preprocess a unification YAML file.
    
    Args:
        file_path: Path to the YAML file
        
    Returns:
        Dictionary with the loaded and preprocessed configuration
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        yaml.YAMLError: If the YAML is invalid
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    if not isinstance(data, dict):
        raise ValueError("YAML file must contain a dictionary at the root level")
    
    # Preprocess the data to match expected structure
    processed_data = preprocess_unification_config(data)
    
    return processed_data


def preprocess_unification_config(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Preprocess unification configuration data.
    
    This function normalizes the YAML structure to match what the Ruby models expect,
    handling things like expanding key_columns relationships and normalizing field names.
    
    Args:
        data: Raw configuration dictionary
        
    Returns:
        Preprocessed configuration dictionary
    """
    result = {
        'name': data.get('name', ''),
        'keys': [],
        'tables': [],
        'canonical_ids': [],
        'persistent_ids': [],
        'master_tables': []
    }
    
    # Process keys section
    if 'keys' in data:
        result['keys'] = [process_key(key) for key in data['keys']]
    
    # Process tables section
    if 'tables' in data:
        result['tables'] = [process_table(table) for table in data['tables']]
    
    # Process canonical_ids section
    if 'canonical_ids' in data:
        result['canonical_ids'] = [process_canonical_id(cid) for cid in data['canonical_ids']]
    
    # Process persistent_ids section  
    if 'persistent_ids' in data:
        result['persistent_ids'] = [process_persistent_id(pid) for pid in data['persistent_ids']]
    
    # Process master_tables section
    if 'master_tables' in data:
        result['master_tables'] = [process_master_table(mt) for mt in data['master_tables']]
    
    return result


def process_key(key_data: Dict[str, Any]) -> Dict[str, Any]:
    """Process a single key definition."""
    result = {
        'name': key_data.get('name', ''),
        'valid_regexp': key_data.get('valid_regexp'),
        'invalid_texts': key_data.get('invalid_texts')
    }
    
    # Remove None values
    return {k: v for k, v in result.items() if v is not None}


def process_table(table_data: Dict[str, Any]) -> Dict[str, Any]:
    """Process a single table definition."""
    result = {
        'database_name': table_data.get('database', ''),
        'table_name': table_data.get('table', ''), 
        'as_name': table_data.get('as', table_data.get('table', '')),  # default as_name to table_name
        'incremental_columns': table_data.get('incremental_columns'),
        'key_columns': table_data.get('key_columns', [])
    }
    
    # Remove None values
    return {k: v for k, v in result.items() if v is not None}


def process_canonical_id(cid_data: Dict[str, Any]) -> Dict[str, Any]:
    """Process a single canonical_id definition."""
    result = {
        'name': cid_data.get('name', ''),
        'do_not_merge_key': cid_data.get('do_not_merge_key'),
        'merge_by_canonical_ids': cid_data.get('merge_by_canonical_ids', []),
        'merge_by_keys': cid_data.get('merge_by_keys', []),
        'source_tables': cid_data.get('source_tables'),
        'merge_iterations': cid_data.get('merge_iterations', 3),
        'incremental_merge_iterations': cid_data.get('incremental_merge_iterations', 2)
    }
    
    # Remove None values  
    return {k: v for k, v in result.items() if v is not None}


def process_persistent_id(pid_data: Dict[str, Any]) -> Dict[str, Any]:
    """Process a single persistent_id definition."""
    result = {
        'name': pid_data.get('name', ''),
        'merge_by_persistent_ids': pid_data.get('merge_by_persistent_ids', []),
        'merge_by_keys': pid_data.get('merge_by_keys', []),
        'source_tables': pid_data.get('source_tables'),
        'merge_iterations': pid_data.get('merge_iterations', 3),
        'incremental_merge_iterations': pid_data.get('incremental_merge_iterations', 2)
    }
    
    # Remove None values
    return {k: v for k, v in result.items() if v is not None}


def process_master_table(mt_data: Dict[str, Any]) -> Dict[str, Any]:
    """Process a single master_table definition."""
    result = {
        'name': mt_data.get('name', ''),
        'canonical_id': mt_data.get('canonical_id'),
        'persistent_id': mt_data.get('persistent_id'),
        'attributes': []
    }
    
    # Process attributes
    if 'attributes' in mt_data:
        result['attributes'] = [process_attribute(attr) for attr in mt_data['attributes']]
    
    # Remove None values
    return {k: v for k, v in result.items() if v is not None}


def process_attribute(attr_data: Dict[str, Any]) -> Dict[str, Any]:
    """Process a single attribute definition."""
    result = {
        'name': attr_data.get('name', ''),
        'array_elements': attr_data.get('array_elements'),
        'source_canonical_id': attr_data.get('source_canonical_id'),
        'source_persistent_id': attr_data.get('source_persistent_id'),
        'valid_regexp': attr_data.get('valid_regexp'),
        'invalid_texts': attr_data.get('invalid_texts'),
        'source_columns': []
    }
    
    # Process source_columns
    if 'source_columns' in attr_data:
        result['source_columns'] = [process_source_column(sc) for sc in attr_data['source_columns']]
    
    # Remove None values
    return {k: v for k, v in result.items() if v is not None}


def process_source_column(sc_data: Dict[str, Any]) -> Dict[str, Any]:
    """Process a single source_column definition."""
    result = {
        'relation_table_as_name': sc_data.get('table', ''),
        'column': sc_data.get('column', ''),
        'priority': sc_data.get('priority'),
        'order_type': sc_data.get('order')
    }
    
    # Remove None values
    return {k: v for k, v in result.items() if v is not None}