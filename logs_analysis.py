#!/usr/bin/env python3
import psycopg2

# Define report file name and database name
FILENAME = "report.txt"
DBNAME = "news"
connection = None

# Create lists of questions, queries, answer_templates
questions = [
    "\n1. What are the most popular three articles of all time?\n",
    "\n2. Who are the most popular article authors of all time?\n",
    "\n3. On which days did more than 1% of requests lead to errors?\n"
]

queries = [
    "SELECT title, num_of_requests FROM article_popularity LIMIT 3",
    "SELECT author_name, total_views FROM author_popularity",
    "SELECT log_date, error_rate FROM error_report WHERE error_rate > 0.01"
]

answer_templates = [
    "  * {} - {:,} views\n",
    "  * {} - {:,} views\n",
    "  * {:%b %d, %Y} - {:.2%} errors\n"
]


def connect(database_name):
    """ Connect to the PostgreSQL database.
        Returns a database connection.
    """
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        c = db.cursor()
        return db, c
    except psycopg2.Error as e:
        print("\nUnable to connect to database: {}".format(database_name))
        raise e


def get_query_results(database_name, query):
    """ Get query results from the PostgreSQL database.
        Returns a list of tuples of the query results.
    """
    db = None
    try:
        db, c = connect(database_name)
        c.execute(query)
        return c.fetchall()

    except psycopg2.Error as e:
        print("\nUnable to get query results from database.")
        raise e

    finally:
        db.close()


if __name__ == "__main__":
    # Open report file : FILENAME
    with open(FILENAME, "w") as report_file:

        # Print header line on report file and stdout
        print("\n### Udacity FSND - Log Analysis project ###\n")
        report_file.write(
            "***** FSND - Logs Analysis project by Young Jung *****\n")

        # Write questions and answers on report from Q1 to Q3
        print("fetching data from the database ..", end="", flush=True)
        for index in range(len(questions)):
            query_results = None

            # Print question on report file
            report_file.write(questions[index])

            # Fetch data from the database
            try:
                query_results = get_query_results(DBNAME, queries[index])

            except psycopg2.Error as e:
                # Print error messages on report file and stdout
                report_file.write("\nOops.. Something went wrong.")
                report_file.write("\nCouldn't generate logs report... Sorry.")
                print(e)

            else:
                # Print answers on report file
                for result in query_results:
                    report_file.write(
                        answer_templates[index].format(result[0], result[1]))
                print("..", end="", flush=True)


#
# try:
#     # Connect to Database - DBNAME
#     print("connecting to database: {} ... ".format(DBNAME), end="", flush=True)
#     connection = psycopg2.connect(database=DBNAME)
#     cursor = connection.cursor()
#     print("OK", end="\n", flush=True)
#
#     # Write questions and answers on report from Q1 to Q3
#     print("fetching data from the database ..", end="", flush=True)
#     for index in range(len(questions)):
#         # Print question on report file
#         report_file.write(questions[index])
#
#         # Fetch data from the database
#         cursor.execute(queries[index])
#         results = cursor.fetchall()
#         print("..", end="", flush=True)
#
#         # Print answers on report file
#         for result in results:
#             report_file.write(
#                 answer_templates[index].format(result[0], result[1]))
#
# except psycopg2.Error as e:
#     # Print error messages on report file and stdout
#     report_file.write("\nOops.. Something went wrong.")
#     report_file.write("\nCouldn't generate logs report... Sorry.")
#     print("FAILED", end="\n", flush=True)
#     print(e)
#
# else:
#     # Print report messages on stdout
#     print(" OK", end="\n", flush=True)
#     print("\n### Report File is ready. ###")
#     print("### Check out \033[1m{}\033[0m file. ###\n".format(FILENAME))
#
# finally:
#     # Close connection and report file
#     if connection:
#         connection.close()
#     report_file.close()
