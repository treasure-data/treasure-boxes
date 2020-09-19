function (user, context, callback) {
    user.app_metadata = user.app_metadata || {};
    if (user.app_metadata.signedup) return callback(null, user, context);
    let request = require('request');
    let body = {
        auth0_user_id: user.user_id,
        auth0_tenant: context.tenant,
      	email: user.email
        // and user.user_metadata, user.app_metadata, etc.
    };

    // It's for the debug to display on the logs stream
    console.log(JSON.stringify(body, null, 2));

    // Set your TD's environment info
    let option = {
        // Set the destination Endpoint, DB name and, Table name
        // Endpoint: https://tddocs.atlassian.net/wiki/spaces/PD/pages/1085143/Sites+and+Endpoints (JS/Mobile SDK/Postback part)
        url: 'https://{ENDPOINT}/postback/v3/event/{YOUR_DB}/{YOUR_TABLE}',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            // Set your TD Write key
            'X-TD-Write-Key': '{TD_WRITE_API_KEY}'
            // You can also use the Secrets feature of Auth0 to configure it as follows
            // 'X-TD-Write-Key': configuration.td_write_key
        },
        body: JSON.stringify(body)
    };
    request(option, (error, response, body) => {
        user.app_metadata.signedup = true;
        auth0.users.updateAppMetadata(user.user_id, user.app_metadata);
        return callback(null, user, context);
    });
}