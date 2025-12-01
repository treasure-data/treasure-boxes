# Activation Actions Examples

This directory contains sample workflows for Treasure Data's Activation Actions feature.

## What is Activation Actions?

Activation Actions enables you to run a user-defined custom workflow to execute desired actions during an activation process. An instance of this workflow is triggered automatically during every activation event. The overall status of the activation is tied to this integrated workflow. The activation would have a successful status only when both the activation and triggered workflow are successful.

For more details about Activation Actions, please refer to the [official documentation](https://docs.treasuredata.com/articles/#!pd/activation-actions).

## Available Examples

### 1. [filter_by_target_list](./filter_by_target_list)
Filter a Parent Segment by joining with a target list table using anonymous_id. This example demonstrates:
- Using String Builder to pass custom parameters
- Cross-database JOIN between Parent Segment and target table
- Returning all columns from Parent Segment for filtered records

### 2. [hashed_email](./hashed_email)
Hash email addresses in the activation output.

### 3. [incremental_wf](./incremental_wf)
Incremental activation that tracks only new (`add`) and removed (`delete`) profiles between activation runs.

### 4. [restrict_and_add_column](./restrict_and_add_column)
Restrict profiles using filters in the custom workflow and add additional columns to the output.

## Common Parameters

Activation Actions provides built-in parameters that are automatically passed to your workflow:

- `activation_actions_db`: Database name where Parent Segment is stored
- `activation_actions_table`: Parent Segment table name (fully qualified: `database.table`)

You can also define custom parameters using String Builder in the Activation Actions configuration.

For a complete list of available parameters, see the [Activation Actions Parameters documentation](https://docs.treasuredata.com/articles/#!pd/activation-actions-parameters).

## Getting Started

1. Choose an example that matches your use case
2. Upload the workflow to Treasure Data: `td wf push <workflow_name>`
3. Configure Activation Actions in Audience Studio:
   - Set the workflow as a custom workflow
   - Configure any required custom parameters
4. Test the activation to verify the results

## Contributing

To add a new example:
1. Create a new directory under `activation_actions/`
2. Include a README.md with clear documentation
3. Provide sample queries and workflow definition
4. Update this README to list the new example
