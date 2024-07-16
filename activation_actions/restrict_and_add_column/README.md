## Restrict and Add Column using Custom Workflow for Activation Actions

Activation Actions enables you to run a user-defined custom workflow to execute these desired actions during an activation process. An instance of this workflow is triggered automatically during every activation event. The overall status of the activation is tied to this integrated workflow. The activation would have a successful status only when both the activation and triggered workflow are successful. By using a custom workflow within the Activation process, you can extend and customize your data activation capabilities to meet specific operational needs.

For more detail about Activation Actions, please refer to [this doc](https://docs.treasuredata.com/articles/#!pd/activation-actions).

This sample code restricts the profiles output by using a filter in Custom Workflow for Activaiton Actions.

### How to use

1. Download this folder into your local.
2. Upload the workflow `td wf push td_load_gcs` (Require td command installation)
3. Set `restrict_and_add_column.dig` as a custom workflow of the Activation Action in Audience Studio.

## Available Parameters for Activation Actions

On Treasure Workflow, various built-in parameters are available for Workflow and SQL files. Please refer to [Doc](https://docs.treasuredata.com/articles/#!pd/activation-actions-parameters)
