# Workflow: http for Chatwork Example

This example workflow notifies calculated data from TreasureData to Chatwork, using [http](http://docs.digdag.io/operators/http.html) operator.

# Preparation

This example workflow uses [Chatwork API](http://developer.chatwork.com/ja/endpoints.html).

Ex. https://api.chatwork.com/v2/rooms/...


# How to Run

First, you need to upload the workflow.

    # Upload
    $ td wf push td_chatwork_example

Now, you can trigger the session manually.
    
    # Run
    $ td wf start td_chatwork_example chatwork_mention --session now

# Results

This example workflow would send the following message.

![chatwork](https://gyazo.com/73c26d66ab9f16089dde84913f11b08c)
    
# Next Step

If you have any questions, please contact support@treasure-data.com.
