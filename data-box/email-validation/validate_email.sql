SELECT
${td.column},

-- makes sure there is 1 and only 1 @ symbol .
CASE WHEN CARDINALITY(SPLIT(${td.column}, '@')) != 2

-- email is not null
OR ${td.column} IS NULL

-- only have ASCII characters in in any portion of the email address
OR REGEXP_LIKE(${td.column}, '^[\x21-\x7E]+$') = false

-- the @ symbol is not the first character in the email address or the last
OR SUBSTR(${td.column}, 1, 1) = '@'
OR SUBSTR(${td.column}, LENGTH(${td.column}), 1) = '@'

-- a period is not the first or last character in the email
OR SUBSTR(${td.column}, 1, 1) = '.'
OR SUBSTR(${td.column}, LENGTH(${td.column}), 1) = '.'

-- email address is > 6 characters
OR LENGTH(${td.column}) <= 6

-- makes sure there are no ( , \  ; * # ") in the email address
OR LENGTH(REGEXP_REPLACE(${td.column}, ',|;|#|\*|\\|\"| ')) != LENGTH(${td.column})

-- the email should be formatted as x@x.xx 
OR REGEXP_LIKE(${td.column}, '..*@..*\...*') = false

-- the email should follow RFC 5322
OR REGEXP_LIKE(${td.column}, '^[A-Z0-9._%-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$') = true

THEN 0
ELSE 1 END AS valid_email
FROM ${td.database}.${td.table}
