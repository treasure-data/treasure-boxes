module.exports = function (user, context, cb) {

    // To use this module, you must first install it on the UI
    let request = require('request');

    // Set items you want to sent to TD
    let data = {
        auth0_user_id: user.id,
        auth0_tenant: user.tenant,
        email: user.email,
        email_verified: user.emailVerified
        // and user.user_metadata, user.app_metadata, etc.
    };

    // It's for the debug to display on the logs stream
    console.log(JSON.stringify(data, null, 2));

    // Set your TD's environment info
    let options = {
        // Set the destination Endpoint, DB name and, Table name
        // Endpoint: https://docs.treasuredata.com/display/public/PD/Sites+and+Endpoints (JS/Mobile SDK/Postback part)
        url: 'https://{ENDPOINT}/postback/v3/event/{YOUR_DB}/{YOUR_TABLE}',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            // Set your TD Write key
            'X-TD-Write-Key': '{TD_WRITE_API_KEY}'
            // You can also use the Secrets feature of Auth0 to configure it as follows
            // 'X-TD-Write-Key': context.webtask.secrets.td_write_apikey
        },
        body: JSON.stringify(data)
    };
    request.post(options, function(error, response, body){
        if (!error && response.statusCode === 200) {
            console.log(body.name);
        } else {
            console.log('error: ' + response.statusCode);
        }
    });

    // Perform any asynchronous actions
    cb();
};