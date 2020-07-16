# Traveloka

write a simple validator for simple BigQuery queries:

- no where statement only select & agregated statement and group by
- make sure the query is valid

Please note that this is only naive implementation. The correct way to do it
will be using SQL parser, or use the BigQuery API directly to validate the SQL.

## Unit Test

Run the following command to run the unit test:

    python3 validator_test.py
