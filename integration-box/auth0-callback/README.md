# Integration of Auth0 with Treasure Data by Auth0's callback features

[Auth0](https://auth0.com/) is a cloud service vendor that provides authentication and authorization mechanisms. This page introduces callback integration with TD by streaming using Auth0's Rules and Hooks.



# Prerequisites
### Auth0
- Rules and Hooks, which are features of Auth0, must be available.

### Treasure Data
- Create a database dedicated for this integration. (no need to create tables)
- Generate an TD API Key with write-key permission. (Plazma CDP)
    - If you use ADL which is one of our product, you need to set master-key. Please contact support@treasure-data.com for the product detail.

# Features description
### Rules (Auth0)
This is a JavaScript function that can be executed upon authentication in Auth0. The completion of the authentication process triggers the execution of the rule (a JavaScript function written by the user) that has already been created.

Please see detail:
https://auth0.com/docs/rules

### Hooks (Auth0)
Please see:
https://auth0.com/docs/hooks

### Postback API (TD)
Treasure Data users can ingest data through the public REST API. You can use Treasure Data to create custom webhooks into your data.

Please see:
https://tddocs.atlassian.net/wiki/spaces/PD/pages/1083818/Postback+API


# Sample
### Trigger: Post User Registration
This is a sample to call back id, email, and etc. obtained by Auth0 after sign-up to TD.

- [Rules](./Rules/sample_rules_post-user-registration.js)
- [Hooks](./Hooks/sample_hooks_post-user-registration.js)