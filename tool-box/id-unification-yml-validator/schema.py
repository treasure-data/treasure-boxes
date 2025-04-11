{
    "name": {"required": True, "type": "string"},
    "keys": {
        "required": True,
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "name": {"required": True, "type": "string"},
                "valid_regexp": {"type": "string"},
                "invalid_texts": {"type": "list"},
            },
        },
    },
    "tables": {
        "required": True,
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "database": {"required": True, "type": "string"},
                "table": {"type": "string"},
                "as": {"type": "string"},
                "incremental_columns": {"type": "list"},
                "key_columns": {
                    "type": "list",
                    "schema": {
                        "type": "dict",
                        "schema": {
                            "column": {"type": "string"},
                            "key": {"type": "string"},
                        },
                    },
                },
            },
        },
    },
    "canonical_ids": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "name": {"type": "string"},
                "merge_by_keys": {"type": "list"},
                "merge_by_canonical_ids": {"type": "list"},
                "source_tables": {"type": "list"},
                "merge_iterations": {"type": "integer", "min":0, "max":50},
                "incremental_merge_iterations": {"type": "integer", "min":0, "max":50},
            },
        },
    },
    "master_tables": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "name": {"type": "string"},
                "canonical_id": {"type": "string"},
                "attributes": {
                    "type": "list",
                    "schema": {
                        "type": "dict",
                        "schema": {
                            "name": {"type": "string"},
                            "source_canonical_id": {"type": "string"},
                            "source_columns": {
                                "type": "list",
                                "schema": {
                                    "type": "dict",
                                    "schema": {
                                        "table": {"type": "string"},
                                        "column": {"type": "string"},
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    },
}
