# Workflow: td example (Result Output to FTP(S))

This example workflow ingests data in daily basis, using [Treasure Data's Writing Job Results into FTP(S)](https://docs.treasuredata.com/articles/result-into-ftp) with [td](http://docs.digdag.io/operators/td.html) operator.

# How to Run

First, please upload your workflow project by `td wf push` command.

    # Upload
    $ td wf push td_ftp

Second, please set ftp credentials by `td wf secrets` command.

    # Set Secrets
    $ td wf secrets --project td_ftp --set ftp_password=xyzxyzxyzxyz

    # Set Secrets on your local for testing
    $ td wf secrets --local --set ftp_password=xyzxyzxyzxyz

Now you can reference these credentials by `${secret:}` syntax in the dig file.

You can trigger the session manually.

    # Run
    $ td wf start td_ftp td_ftp --session now
    
# Supplemental

JSON format of Result Output to FTP(S) is the followings.

- FTP: '{"type":"ftp","host":"xx.xx.xx.xx","port":21,"username":"xxxx","password":"xxxxx","path_prefix":"/path/to/file","file_ext":".csv","sequence_format":"","header_line":true,"quote_policy":"MINIMAL","delimiter":",","null_string":"","newline":"CRLF"}'
- FTPS: '{"type":"ftp","host":"xx.xx.xx.xx","port":990,"username":"xxxx","password":"xxxxx","passive_mode":true,"ascii_mode":true,"ssl":true,"ssl_explicit":false,"ssl_verify":false,"ssl_verify_hostname":false,"path_prefix":"/path/to/file","file_ext":".csv","sequence_format":"","header_line":true,"quote_policy":"MINIMAL","delimiter":",","null_string":"","newline":"CRLF"}'
- FTPES: '{"type":"ftp","host":"xx.xx.xx.xx","port":21,"username":"xxxx","password":"xxxxx","passive_mode":true,"ascii_mode":true,"ssl":true,"ssl_explicit":true,"ssl_verify":false,"ssl_verify_hostname":false,"path_prefix":"/path/to/file","file_ext":".csv","sequence_format":"","header_line":true,"quote_policy":"MINIMAL","delimiter":",","null_string":"","newline":"CRLF"}'

For more details, please see [Treasure Data documentation](https://docs.treasuredata.com/articles/result-into-ftp#usage-from-cli)

# Next Step

If you have any questions, please contact support@treasure-data.com.
