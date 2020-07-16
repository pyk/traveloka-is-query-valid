# This script is a naive implementation of SQL query validation
# The best approach should use SQL parser instead of manually checking every token
AGREGATE_STATEMENT = ["count", "sum"]
REQUIRED_STATEMENT = ["select", "from"]
VALID_STATEMENT = ["select", "from", "group"]
BLOCKED_STATEMENT = ["where"]

# Given bigquery SQL make sure the query is valid and there is no WHERE statement
def is_query_valid_sql(query: str) -> bool:
    # Normalize the query first
    normalized_query = query.lower().strip()

    # Make sure there is no blocket statement
    raw_tokens = normalized_query.split(" ")
    tokens = []
    for token in raw_tokens:
        for subtoken in token.split(","):
            if subtoken != "":
                tokens.append(subtoken)

    for token in BLOCKED_STATEMENT:
        if token in tokens:
            return False

    # Make sure there are required statements
    for token in REQUIRED_STATEMENT:
        if token not in tokens:
            return False

    # Nake sure SELECT and FROM is syntatically valid
    selected_columns = []
    for i, sql_token in enumerate(tokens):
        next_token = None
        if i < (len(tokens)-1):
            next_token = tokens[i+1].split(",")[0]

        if sql_token == "select":
            # The next token should be name of column
            if next_token is None or next_token in VALID_STATEMENT:
                return False
            # Collect column names
            for column_name in tokens[i+1:]:
                if column_name == "from":
                    break
                selected_columns.append(column_name)

        if sql_token == "from":
            # The next token should be name of table
            if next_token is None or next_token in VALID_STATEMENT:
                return False

        if sql_token == "group":
            # next token should by
            if next_token is None or next_token != "by":
                return False

        if sql_token == "by":
            # Next token should exists in the previous statement
            # unless it is a number
            if next_token is None:
                return None
            if not next_token.isnumeric():
                if next_token not in selected_columns:
                    return False
            # TODO(bayu): Get the number of grouped columns, make sure it is
            # len(grouped_columns) < len(selected_columns) - 1

    # Make sure if there is any agregate statement then the previous field should be grouped
    for token in tokens:
        for agg in AGREGATE_STATEMENT:
            if agg in token:
                # The GROUP BY should exists
                if "group" in tokens:
                    return True
                else:
                    return False
    return True
