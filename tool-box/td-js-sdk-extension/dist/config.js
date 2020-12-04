// Init TD JS SDK
var td = new Treasure({
    database: 'your_db_name',
    writeKey: 'your_api_write_key',
    host: 'in.treasuredata.com',
    sscDomain: 'your.domain',
    sscServer: 'ssc.your.domain',
    useServerSideCookie: false,
    startInSignedMode: true
});

td.set('$global', 'td_global_id', 'td_global_id');

// Track everything by TD JS SDK Extension
(function () {
    // Cut the mustard
    if ('addEventListener' in window &&
        'td' in window &&
        'tdext' in window
    ) {
        // Init TD Extension
        tdext.init({
            table: 'weblog',
            eventName: 'TDExtRecurringEvent',
            eventFrequency: 250,
            targetWindow: 'self',
            tdNs: 'td',
            options: {
                session: {
                    enable: true,
                    domain: 'example.com',
                    lifetime: 1800
                },
                unload: {
                    enable: true
                },
                clicks: {
                    enable: true,
                    targetAttr: 'data-trackable'
                },
                scroll: {
                    enable: true,
                    threshold: 2,
                    granularity: 20,
                    unit: 'percent'
                },
                read: {
                    enable: true,
                    threshold: 2,
                    granularity: 20,
                    target: window.document.getElementById('article')
                },
                media: {
                    enable: true,
                    heartbeat: 5
                },
                form: {
                    enable: true,
                    targets: [].slice.call(window.document.getElementsByTagName('form'))
                }
            }
        });

        // Track PV
        tdext.trackPageview();

        // Custom Action (if you want to track events other than auto-tracked, use this snippet)
        /*
        tdext.trackAction(
            'action',
            'category',
            {
                custom_variable: 'something_value'
            },
            function () {
                console.log("sending data to TD has been succeeded.");
            },
            function () {
                console.log("failed to send data to TD.");
            }
        );
        */
    }
}());
