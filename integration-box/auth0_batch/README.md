# Auth0 User integration

This is a sample workflow to ingest user data stored in [Auth0](https://auth0.com/).

This workflow uses [Auth0 Export users job API](https://auth0.com/docs/api/management/v2/#!/Jobs/post_users_exports), ingesting all users in Auth0 to TreasureData.

## How to use

You need to edit the variables respectively in the `export.dig` for your environment.

Then push this workflow project to Treasure Data.

```
$ td wf push auth0_batch
```

Set workflow secrets. Details are shown in the below section.

```
$ td wf secrets --set auth0.client_id --project auth0_batch
$ td wf secrets --set auth0.client_secret --project auth0_batch
$ td wf secrets --set td.apikey --project auth0_batch
```

Then run the workflows using CLI, or TD workflow console.

```
$ td wf start auth0_batch export --session now
```

## Secrets

You need to setup the following secrets

- `td.endpoint` : Provide master APIKEY
- `auth0.client_id`
- `auth0.client_secret`