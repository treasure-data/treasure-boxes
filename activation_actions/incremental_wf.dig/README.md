# Incremental Activation as a Custom workflow for Activation Actions

Activation Actions enables you to run a user-defined custom workflow to execute these desired actions during an activation process. An instance of this workflow is triggered automatically during every activation event. The overall status of the activation is tied to this integrated workflow. The activation would have a successful status only when both the activation and triggered workflow are successful. By using a custom workflow within the Activation process, you can extend and customize your data activation capabilities to meet specific operational needs.

For more detail about Activation Actions, please refer to [this doc](https://docs.treasuredata.com/articles/#!pd/activation-actions).

This example code considers `add` (new profiles) and `delete` (dropped profiles) changes only from your activated profiles. When there is no difference between the profile of the current run and the previous run, the diff table won’t be generated. The attributes used here (e.g., profile_id) are just for example - user may have to use their attributes in the queries according to the data schema in the context

## How to use this workflow for Activation Actions

1. Download this folder into your local.
2. Upload the workflow `td wf push td_load_gcs` (Require td command installation)
3. Set `incremental_wf.dig` as a custom workflow of the Activation Action in Audience Studio.

## Available Parameters for Activation Actions

On Treasure Workflow, various built-in parameters are available for Workflow and SQL files. Please refer to [Doc](https://docs.treasuredata.com/articles/#!pd/activation-actions-parameters)
