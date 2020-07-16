import unittest

import validator

class TestBigQuerySqlValidation(unittest.TestCase):
    def test_valid_sql(self):
        valid_1 = """
            SELECT * FROM something;
        """

        valid_2 = """
            SELECT name_where FROM something;
        """

        valid_3 = """
            SELECT name, COUNT(UNIQUE(id)) FROM table GROUP BY 1
        """

        valid_sqls = [valid_1, valid_2, valid_3]
        for valid_sql in valid_sqls:
            self.assertTrue(validator.is_query_valid_sql(valid_sql))

    def test_invalid_sql(self):
        # Invalid contains WHERE statement
        invalid_1 = """
            SELECT * FROM something WHERE ab = 1;
        """
        invalid_2 = """
            select * from something WHERE ab = 2;
        """

        # Invalid contains agregator but there is no group
        invalid_3 = """
            select foo, count(*) FROM something
        """

        # Invalid contains group by that doesn't exists
        invalid_4 = """
            SELECT foo, count(*) FROM table GROUP BY bar
        """

        # Invalid sql
        invalid_5 = """
            test
        """
        invalid_6 = """
            select from
        """
        invalid_7 = """
            select foo from bar group
        """
        invalid_8 = """
            select foo from bar group by
        """
        invalid_9 = """
            select foo from group by
        """

        invalid_sqls = [invalid_1, invalid_2, invalid_3, invalid_4, invalid_5, invalid_6, invalid_7, invalid_8, invalid_9]
        for invalid_sql in invalid_sqls:
            self.assertFalse(validator.is_query_valid_sql(invalid_sql))


if __name__ == "__main__":
    unittest.main()