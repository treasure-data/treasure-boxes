SELECT time, id, name
FROM test_table
WHERE TD_INTERVAL(time, '-5d')