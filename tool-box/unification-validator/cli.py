#!/usr/bin/env python3
"""
CLI tool for validating ID Unification YAML files.

This tool validates unification YAML files using comprehensive Pydantic models.
"""

import sys
import argparse
from pathlib import Path
from typing import Dict, Any

import yaml
from pydantic import ValidationError

from models import Unification
from yaml_loader import load_unification_yaml


def format_validation_errors(errors: list, data: dict = None) -> str:
    """Format Pydantic validation errors grouped by object for better readability."""
    # Group errors by their base object (e.g., tables[3], master_tables[0])
    grouped_errors = {}
    
    for error in errors:
        formatted_location = format_error_location(error['loc'], data)
        
        # Remove "Value error, " prefix from message
        message = error['msg']
        if message.startswith("Value error, "):
            message = message[13:]  # Remove "Value error, " prefix
        
        # Special handling for canonical_ids/persistent_ids requirement
        if formatted_location == "General" and "either canonical_ids or persistent_ids must have at least one item" in message:
            formatted_location = "❌ canonical_ids/persistent_ids"
        
        if formatted_location not in grouped_errors:
            grouped_errors[formatted_location] = []
        grouped_errors[formatted_location].append(message)
    
    # Format the grouped errors
    formatted_sections = []
    group_items = list(grouped_errors.items())
    
    for i, (group_key, group_errors) in enumerate(group_items):
        if group_key == "General" or " -> " in group_key:
            # For general errors or complex paths, use the old format
            for error_entry in group_errors:
                formatted_sections.append(f"  {group_key}: {error_entry}")
        elif group_key.startswith("❌ "):
            # For special groups that already have emoji, don't add another one
            formatted_sections.append(f"  {group_key}:")
            for error_entry in group_errors:
                formatted_sections.append(f"    - {error_entry}")
        else:
            # For object-specific errors, use the grouped format
            formatted_sections.append(f"  ❌ {group_key}:")
            for error_entry in group_errors:
                formatted_sections.append(f"    - {error_entry}")
        
        # Add blank line between different objects (except after the last one)
        if i < len(group_items) - 1:
            formatted_sections.append("")
    
    return "\n".join(formatted_sections)


def format_error_location(loc_tuple, data=None):
    """Format error location with proper object[index] (name: "x") format."""
    if not loc_tuple:
        return "General"
    
    # For nested locations like ('master_tables', 0, 'attributes', 6), group under master_table
    if len(loc_tuple) == 4 and loc_tuple[0] == 'master_tables' and loc_tuple[2] == 'attributes':
        mt_index = loc_tuple[1]
        attr_index = loc_tuple[3]
        
        # Get master table name
        mt_name = ""
        if (data and 'master_tables' in data and 
            mt_index < len(data['master_tables']) and 
            isinstance(data['master_tables'][mt_index], dict)):
            mt_name = data['master_tables'][mt_index].get('name', '')
        
        # Return just the master table as the group key - the attribute info will be in the message
        return f"master_tables[{mt_index}] (name: \"{mt_name}\")" if mt_name else f"master_tables[{mt_index}]"
    
    # For simpler locations, use the original logic
    location_parts = []
    
    for i, loc in enumerate(loc_tuple):
        if isinstance(loc, int) and i > 0:
            # This is an array index, try to get the name
            prev_loc = loc_tuple[i-1]
            
            # Navigate to the correct location in the data
            nav_data = data
            for j in range(i-1):
                path_part = loc_tuple[j]
                if isinstance(nav_data, dict) and path_part in nav_data:
                    nav_data = nav_data[path_part]
                elif isinstance(nav_data, list) and isinstance(path_part, int) and path_part < len(nav_data):
                    nav_data = nav_data[path_part]
                else:
                    nav_data = None
                    break
            
            # Check if we have an array and can get the name
            if (isinstance(nav_data, dict) and 
                prev_loc in nav_data and 
                isinstance(nav_data[prev_loc], list)):
                items = nav_data[prev_loc]
                if (loc < len(items) and 
                    isinstance(items[loc], dict) and 
                    'name' in items[loc]):
                    name = items[loc]['name']
                    return f"{prev_loc}[{loc}] (name: \"{name}\")"
                else:
                    return f"{prev_loc}[{loc}]"
            else:
                return f"{prev_loc}[{loc}]"
        else:
            location_parts.append(str(loc))
    
    return " -> ".join(location_parts)


def validate_yaml_file(file_path: Path) -> tuple[bool, str]:
    """
    Validate a unification YAML file.
    
    Returns:
        tuple: (is_valid, message)
    """
    try:
        # Load and parse the YAML file
        data = load_unification_yaml(file_path)
        
        # Try to validate using Pydantic model
        # This will collect all field-level validation errors
        unification = Unification(**data)
        
        # Even if Pydantic validation passes, check for additional issues
        additional_errors = collect_additional_errors(data)
        if additional_errors:
            # If there are additional errors, format them
            error_msg = f"Validation failed for '{file_path}':\n"
            error_msg += "─" * 50 + "\n"
            error_msg += "VALIDATION WARNINGS:\n"
            error_msg += format_validation_errors(additional_errors, data)
            return False, error_msg
        
        return True, f"✅ Validation successful! File '{file_path}' is valid."
        
    except FileNotFoundError:
        return False, f"❌ Error: File '{file_path}' not found."
    
    except yaml.YAMLError as e:
        return False, f"❌ YAML parsing error: {e}"
    
    except ValidationError as e:
        # Separate structural errors from detailed errors
        all_errors = list(e.errors())
        structural_errors = []
        detailed_errors = []
        
        # Check for missing required root objects and structural issues first
        for error in all_errors:
            loc = error['loc']
            msg = error['msg']
            # Clean message for comparison
            if msg.startswith("Value error, "):
                msg = msg[13:]
            
            # Categorize as structural error if:
            # 1. Missing required root objects (name, keys, tables, canonical_ids - but NOT master_tables)
            # 2. Either canonical_ids or persistent_ids requirement
            if (len(loc) == 1 and loc[0] in ['name', 'keys', 'tables', 'canonical_ids']) or \
               (len(loc) == 0 and "either canonical_ids or persistent_ids must have at least one item" in msg):
                structural_errors.append(error)
            else:
                detailed_errors.append(error)
        
        # Try to collect additional validation errors
        try:
            partial_validation_errors = collect_additional_errors(data)
            
            # Only add errors that aren't already in the list
            existing_error_sigs = set()
            for err in all_errors:
                msg = err['msg']
                if msg.startswith("Value error, "):
                    msg = msg[13:]
                existing_error_sigs.add((err['loc'], msg))
            
            for new_error in partial_validation_errors:
                error_sig = (new_error['loc'], new_error['msg'])
                if error_sig not in existing_error_sigs:
                    # Categorize additional errors
                    loc = new_error['loc']
                    msg = new_error['msg']
                    
                    if (len(loc) == 1 and loc[0] in ['name', 'keys', 'tables', 'canonical_ids']) or \
                       (len(loc) == 0 and "either canonical_ids or persistent_ids must have at least one item" in msg) or \
                       ("Table definitions may be missing" in msg):
                        structural_errors.append(new_error)
                    else:
                        detailed_errors.append(new_error)
        except Exception:
            pass
        
        # Format the error message
        error_msg = f"Validation failed for '{file_path}':\n"
        error_msg += "─" * 50 + "\n"
        
        # Show structural errors first
        if structural_errors:
            error_msg += "🔴 STRUCTURAL ISSUES (fix these first):\n"
            error_msg += format_validation_errors(structural_errors, data) + "\n"
        
        # Show detailed errors with warning if structural issues exist
        if detailed_errors:
            if structural_errors:
                error_msg += "\n" + "─" * 50 + "\n"
                error_msg += "⚠️  DETAILED ERRORS (may not be accurate due to structural issues above):\n"
            else:
                error_msg += "VALIDATION ERRORS:\n"
            error_msg += format_validation_errors(detailed_errors, data)
        
        return False, error_msg
    
    except Exception as e:
        return False, f"❌ Unexpected error: {e}"


def collect_additional_errors(data):
    """Try to collect additional validation errors that might be missed by the main validation."""
    additional_errors = []
    
    # Check for structural issues
    
    # Check canonical_ids/persistent_ids requirement
    canonical_ids_count = len(data.get('canonical_ids', []))
    persistent_ids_count = len(data.get('persistent_ids', []))
    if canonical_ids_count == 0 and persistent_ids_count == 0:
        additional_errors.append({
            'type': 'structure_error',
            'loc': (),
            'msg': 'either canonical_ids or persistent_ids must have at least one item',
            'input': data
        })
    
    if 'keys' in data and 'tables' in data:
        empty_keys_count = sum(1 for item in data['keys'] if isinstance(item, dict) and item.get('name') == '')
        tables_count = len(data['tables'])
        
        # If there are many empty keys and no tables, suggest structural issue
        if empty_keys_count > 5 and tables_count == 0:
            additional_errors.append({
                'type': 'structure_error',
                'loc': (),
                'msg': f'Found {empty_keys_count} keys with empty names and 0 tables. Table definitions may be missing from tables section.',
                'input': data
            })
    
    # Check for items with table properties under keys section
    if 'keys' in data:
        for i, item in enumerate(data['keys']):
            if isinstance(item, dict):
                # Check if this item has table-like properties instead of key properties
                has_table_props = any(prop in item for prop in ['database', 'table', 'key_columns', 'as'])
                has_key_props = 'name' in item and item['name']  # Name must not be empty
                
                if has_table_props and not has_key_props:
                    additional_errors.append({
                        'type': 'structure_error',
                        'loc': ('keys', i),
                        'msg': f'item has table properties (database/table/key_columns) but is in keys section - should be in tables section',
                        'input': item
                    })
    
    # Build available names for cross-reference validation
    key_names = set()
    table_as_names = set()
    canonical_id_names = set()
    persistent_id_names = set()
    
    if 'keys' in data:
        for key in data['keys']:
            if isinstance(key, dict) and 'name' in key and key['name']:
                key_names.add(key['name'])
    
    if 'tables' in data:
        for table in data['tables']:
            if isinstance(table, dict) and 'as_name' in table and table['as_name']:
                table_as_names.add(table['as_name'])
            elif isinstance(table, dict) and 'as' in table and table['as']:
                table_as_names.add(table['as'])
    
    if 'canonical_ids' in data:
        for cid in data['canonical_ids']:
            if isinstance(cid, dict) and 'name' in cid and cid['name']:
                canonical_id_names.add(cid['name'])
    
    if 'persistent_ids' in data:
        for pid in data['persistent_ids']:
            if isinstance(pid, dict) and 'name' in pid and pid['name']:
                persistent_id_names.add(pid['name'])
    
    # Build set of keys actually used in tables
    used_key_names = set()
    if 'tables' in data:
        for table in data['tables']:
            if isinstance(table, dict) and 'key_columns' in table:
                for kc in table['key_columns']:
                    if isinstance(kc, dict) and 'key' in kc:
                        used_key_names.add(kc['key'])
    
    # Check that all defined keys are used in tables
    for i, key in enumerate(data.get('keys', [])):
        if isinstance(key, dict) and 'name' in key and key['name']:
            key_name = key['name']
            if key_name not in used_key_names:
                additional_errors.append({
                    'type': 'value_error',
                    'loc': ('keys', i),
                    'msg': f'key "{key_name}" is not used in any table key_columns',
                    'input': key
                })
    
    # Check cross-reference errors for canonical_ids
    if 'canonical_ids' in data:
        for i, cid in enumerate(data['canonical_ids']):
            if isinstance(cid, dict):
                # Check merge_by_keys references
                if 'merge_by_keys' in cid:
                    for key_name in cid['merge_by_keys']:
                        if key_name not in key_names:
                            additional_errors.append({
                                'type': 'value_error',
                                'loc': ('canonical_ids', i),
                                'msg': f'references unknown key "{key_name}"',
                                'input': cid
                            })
                
                # Check merge_by_canonical_ids references
                if 'merge_by_canonical_ids' in cid:
                    for ref_name in cid['merge_by_canonical_ids']:
                        if ref_name not in canonical_id_names:
                            additional_errors.append({
                                'type': 'value_error',
                                'loc': ('canonical_ids', i),
                                'msg': f'references unknown canonical_id "{ref_name}"',
                                'input': cid
                            })
                
                # Check source_tables references
                if 'source_tables' in cid:
                    for table_name in cid['source_tables']:
                        if table_name not in table_as_names:
                            additional_errors.append({
                                'type': 'value_error',
                                'loc': ('canonical_ids', i),
                                'msg': f'references unknown table "{table_name}"',
                                'input': cid
                            })
    
    # Check cross-reference errors for persistent_ids
    if 'persistent_ids' in data:
        for i, pid in enumerate(data['persistent_ids']):
            if isinstance(pid, dict):
                # Check merge_by_keys references
                if 'merge_by_keys' in pid:
                    for key_name in pid['merge_by_keys']:
                        if key_name != 'time' and key_name not in key_names:
                            additional_errors.append({
                                'type': 'value_error',
                                'loc': ('persistent_ids', i),
                                'msg': f'references unknown key "{key_name}"',
                                'input': pid
                            })
                
                # Check merge_by_persistent_ids references
                if 'merge_by_persistent_ids' in pid:
                    for ref_name in pid['merge_by_persistent_ids']:
                        if ref_name not in persistent_id_names:
                            additional_errors.append({
                                'type': 'value_error',
                                'loc': ('persistent_ids', i),
                                'msg': f'references unknown persistent_id "{ref_name}"',
                                'input': pid
                            })
    
    # Check master_table references
    if 'master_tables' in data:
        for i, mt in enumerate(data['master_tables']):
            if isinstance(mt, dict):
                # Check canonical_id reference
                if 'canonical_id' in mt and mt['canonical_id'] not in canonical_id_names:
                    additional_errors.append({
                        'type': 'value_error',
                        'loc': ('master_tables', i),
                        'msg': f'references unknown canonical_id "{mt["canonical_id"]}"',
                        'input': mt
                    })
                
                # Check persistent_id reference
                if 'persistent_id' in mt and mt['persistent_id'] not in persistent_id_names:
                    additional_errors.append({
                        'type': 'value_error',
                        'loc': ('master_tables', i),
                        'msg': f'references unknown persistent_id "{mt["persistent_id"]}"',
                        'input': mt
                    })
    
    # Check table key_columns reference existing keys
    if 'tables' in data:
        for i, table in enumerate(data['tables']):
            if isinstance(table, dict) and 'key_columns' in table:
                for kc in table['key_columns']:
                    if isinstance(kc, dict):
                        key_name = kc.get('key')
                        if key_name and key_name not in key_names:
                            additional_errors.append({
                                'type': 'value_error',
                                'loc': ('tables', i),
                                'msg': f'key_column references unknown key "{key_name}"',
                                'input': table
                            })
    
    # Check master table attribute source_columns table references
    if 'master_tables' in data:
        for i, mt in enumerate(data['master_tables']):
            if isinstance(mt, dict) and 'attributes' in mt:
                for j, attr in enumerate(mt['attributes']):
                    if isinstance(attr, dict) and 'source_columns' in attr:
                        for sc in attr['source_columns']:
                            if isinstance(sc, dict) and 'relation_table_as_name' in sc:
                                table_name = sc['relation_table_as_name']
                                if table_name not in table_as_names:
                                    attr_name = attr.get('name', f'attribute_{j}')
                                    additional_errors.append({
                                        'type': 'value_error',
                                        'loc': ('master_tables', i, 'attributes', j),
                                        'msg': f'attributes[{j}] (name: "{attr_name}"): source_column references unknown table "{table_name}"',
                                        'input': attr
                                    })
    
    # Check master table attribute uniqueness
    if 'master_tables' in data:
        for i, mt in enumerate(data['master_tables']):
            if isinstance(mt, dict) and 'attributes' in mt:
                attribute_names = []
                seen_duplicates = set()  # Track which duplicates we've already reported
                for attr in mt['attributes']:
                    if isinstance(attr, dict) and 'name' in attr:
                        name = attr['name']
                        if name in attribute_names and name not in seen_duplicates:
                            additional_errors.append({
                                'type': 'value_error',
                                'loc': ('master_tables', i),
                                'msg': f'duplicate attribute name "{name}"',
                                'input': mt
                            })
                            seen_duplicates.add(name)  # Don't report the same duplicate again
                        attribute_names.append(name)
    
    return additional_errors


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Validate ID Unification YAML files using Pydantic models",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s unification.yml
  %(prog)s --verbose my_config.yaml
  %(prog)s *.yml  # Validate multiple files
        """
    )
    
    parser.add_argument(
        'files',
        nargs='+',
        type=Path,
        help='YAML files to validate'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Show detailed validation output'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='unification-validator 1.0.0'
    )
    
    args = parser.parse_args()
    
    # Track validation results
    all_valid = True
    results = []
    
    # Validate each file
    for file_path in args.files:
        is_valid, message = validate_yaml_file(file_path)
        results.append((file_path, is_valid, message))
        
        if not is_valid:
            all_valid = False
    
    # Print results
    if len(args.files) == 1:
        # Single file - just print the result
        _, _, message = results[0]
        print(message)
    else:
        # Multiple files - show summary
        print(f"Validating {len(args.files)} files...\n")
        
        for file_path, is_valid, message in results:
            if args.verbose or not is_valid:
                print(message)
            else:
                status = "✅" if is_valid else "❌"
                print(f"{status} {file_path}")
        
        # Summary
        valid_count = sum(1 for _, is_valid, _ in results if is_valid)
        invalid_count = len(results) - valid_count
        
        print(f"\nSummary: {valid_count} valid, {invalid_count} invalid")
    
    # Exit with appropriate code
    sys.exit(0 if all_valid else 1)


if __name__ == '__main__':
    main()