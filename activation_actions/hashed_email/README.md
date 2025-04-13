# 📣 Activation Workflow using Treasure Data CDP

This workflow leverages **Treasure Data CDP's Activation Actions** to enrich user profiles with raw email addresses based on hashed values. It performs a secure join between hashed emails in the activation profile table and raw emails stored in a separate table before activation

## 🛠 Configuration

Update the following parameters before running the workflow:

```yaml
_export:
  td:
    database: '${activation_actions_db}'  # Target database name
  hashed_email_column: 'hashed_email'     # Column name containing hashed email in the activation table
  raw_email_db_table: 'support.profile_table'  # Fully qualified table name with raw email addresses (e.g. database.table)
  raw_email_column: 'email'               # Column name of raw (non-hashed) email
```

## ▶ Activation Logic

The actual activation step is defined in the `+activation_for_added_profiles` task, which runs the `activation.sql` query.

### Query Logic

This SQL query performs the join between the activation table and the raw email table using SHA-256 hashing:

```sql
SELECT t2.email, t1.* 
FROM 
  (SELECT * FROM ${activation_actions_table}) t1
LEFT JOIN
  (SELECT ${raw_email_column} AS email FROM ${raw_email_db_table}) t2
ON t1.hashed_email = TO_HEX(SHA256(TO_UTF8(email)))
```

### Notes:
- This join ensures that **raw email addresses are only used for matching** and not exposed unless they match a hashed profile.
- You can uncomment and configure the following optional settings if needed:
  ```yaml
  # result_connection: ${result_connection_name}
  # result_settings: ${result_connection_settings}
  ```


## ✅ Prerequisites

- The activation table must contain a hashed email column (`SHA-256` hashed, hex-encoded).
- The raw email table must be accessible and contain unhashed emails in a UTF-8 format.
- Make sure the database/table references are correct and permissions are properly configured.


## 📂 File Structure

You'll need to set these files in your new Treasure Workflow project.

- `workflow.dig`: Defines the TD workflow
- `activation.sql`: Contains the SQL logic for profile enrichment and activation

## 🧭 Setting Up Activation in Audience Studio

Here’s how to configure this workflow in the Treasure Data Console (Audience Studio).

1. Create a Segment

Create a new segment or select an existing one in Audience Studio.
Make sure the segment includes the hashed_email column, which should be a SHA-256 encoded hex string.
If you're using a different hashing algorithm, you'll need to modify the SQL accordingly.

2. Configure Activation Actions in the Activation Screen

[![Image from Gyazo](https://t.gyazo.com/teams/treasure-data/0a215fa0dec68d6850ca8da00a756299.png)](https://treasure-data.gyazo.com/0a215fa0dec68d6850ca8da00a756299)

3. Specify the Hashed Email Column in Output Column Mapping

[![Image from Gyazo](https://t.gyazo.com/teams/treasure-data/a6801682e3949e0f77dee06a2f649e00.png)](https://treasure-data.gyazo.com/a6801682e3949e0f77dee06a2f649e00)

[![Image from Gyazo](https://t.gyazo.com/teams/treasure-data/3c2880aa3906c903e9b6624222ed552b.png)](https://treasure-data.gyazo.com/3c2880aa3906c903e9b6624222ed552b)

## Reference

- [Activation Actions Doc](https://docs.treasuredata.com/articles/#!pd/activation-actions)