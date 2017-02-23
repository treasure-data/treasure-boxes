# Workflow: td example (Result Output to SFTP)

This example workflow ingests data in daily basis, using [Treasure Data's Writing Job Results into SFTP](https://docs.treasuredata.com/articles/result-into-sftp) with [td](http://docs.digdag.io/operators/td.html) operator.

# How to Run

First, please set sftp credentials by `td wf secrets` command with json file which has Multiple credentials. For more details, please see **Multiple secrets can be read from a single file in JSON format.** section in [digdag documentation](http://docs.digdag.io/command_reference.html#secrets)

    # Set Secrets
    $ td wf secrets --project td_sftp --set @secrets.json

    # Set Secrets on your local for testing
    $ td wf secrets --local --set @secrets.json

`secret_key_file` has to care Line Feed Code using escape key.

    # secret_key_file format for secret
    "sftp_secret_key_file": "-----BEGIN RSA PRIVATE KEY-----\\\\nProc-Type: 4,ENCRYPTED\\\\nDEK-Info: AAAAAAAAAAAAAAAAAAAAA\\\\n\\\\nBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB\\\\nCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC\\\\nDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD\\\\n-----END RSA PRIVATE KEY-----",

    # Original secret_key_file
      -----BEGIN RSA PRIVATE KEY-----
      Proc-Type: 4,ENCRYPTED
      DEK-Info: AAAAAAAAAAAAAAAAAAAAA

      BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
      CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
      DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD
      -----END RSA PRIVATE KEY-----

Now you can reference these credentials by `${secret:}` syntax in the dig file.

You can upload the workflow and trigger the session manually.

    # Upload
    $ td wf push td_sftp
    
    # Run
    $ td wf start td_sftp td_sftp --session now
    
# Supplemental

JSON format of Result Output to SFTP is the followings.

- result_url: '{"type":"sftp","host":"${sftp.host}","port":${sftp.port},"username":"${sftp.username}","secret_key_file":"{\"content\":\"${secret:sftp_secret_key_file}\"}","secret_key_passphrase":"${secret:sftp_secret_key_passphrase}","user_directory_is_root":${sftp.user_directory_is_root},"path_prefix":"${sftp.path_prefix}_${datetime}","file_ext":"${sftp.file_ext}","sequence_format":"${sftp.sequence_format}","header_line":${sftp.header_line},"quote_policy":"${sftp.quote_policy}","delimiter":"${sftp.delimiter}","null_string":"${sftp.null_string}","newline":"${sftp.newline}"}'

For more details, please see [Treasure Data documentation](https://docs.treasuredata.com/articles/result-into-sftp#usage-from-cli)

# Next Step

If you have any questions, please contact support@treasure-data.com.
