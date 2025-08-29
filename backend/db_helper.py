import mysql.connector
from contextlib import contextmanager
from typing import Iterable, Optional, Dict, Any
from logging_setup import setup_logger

logger=setup_logger('db_helper')

@contextmanager
def get_db_cursor(commit: bool = False):
    """
    Yields a MySQL cursor. If commit=True, commits on success and rolls back on exception.
    Always closes cursor & connection.
    """
    logger.info(f"Connecting to database. Commit mode: {commit}")
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="expense_manager",
    )
    cursor = connection.cursor(dictionary=True)  # rows as dicts
    try:
        yield cursor
        if commit:
            connection.commit()
            logger.info("Transaction committed.")
    except Exception as e:
        logger.error(f"Database error: {e}")
        if commit:
            connection.rollback()
            logger.info("Transaction rolled back.")
        raise
    finally:
        try:
            cursor.close()
        finally:
            connection.close()
        logger.info("Database connection closed.")


def fetch_expenses(expense_date: Optional[str] = None) -> Iterable[Dict[str, Any]]:
    """
    Returns a list of expense rows. If expense_date is None, returns all rows.
    expense_date should be 'YYYY-MM-DD' for a DATE column.
    """
    logger.info(f"Fetching expenses for date: {expense_date}")
    with get_db_cursor(commit=False) as cursor:
        try:
            cursor.execute(
                "SELECT * FROM expenses WHERE expense_date = %s",
                (expense_date,),
            )
            results = cursor.fetchall()
            logger.info(f"Fetched {len(results)} expenses.")
            return results
        except mysql.connector.Error as err:
            logger.error(f"Error fetching expenses: {err}")
            return []
        


def delete_expense_for_date(expense_date: str) -> int:
    """
    Deletes rows for a given date. Returns number of rows deleted.
    """
    logger.info(f"Deleting expenses for date: {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "DELETE FROM expenses WHERE expense_date = %s",
            (expense_date,),
        )
        count = cursor.rowcount
        logger.info(f"Deleted {count} expenses for date: {expense_date}")
        return count


def insert_expense(expense_date: str, amount: float, category: str, notes: Optional[str]) -> int:
    """
    Inserts one expense. Returns number of rows inserted (1 on success).
    """
    logger.info(f"Inserting expense: date={expense_date}, amount={amount}, category={category}, notes={notes}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            """
            INSERT INTO expenses (expense_date, amount, category, notes)
            VALUES (%s, %s, %s, %s)
            """,
            (expense_date, amount, category, notes),
        )
        count = cursor.rowcount
        logger.info(f"Inserted {count} expense(s).")
        return count

def fetch_expense_summary(start_date: str, end_date: str) -> Iterable[Dict[str, Any]]:
    logger.info(f"Fetching expense summary from {start_date} to {end_date}")
    with get_db_cursor(commit=False) as cursor:
        cursor.execute('''SELECT category,SUM(amount) as total FROM expenses WHERE 
        expense_date BETWEEN %s and %s GROUP BY category;''',(start_date, end_date))
        results = cursor.fetchall()
        logger.info(f"Fetched summary for {len(results)} categories.")
        return results


if __name__ == "__main__":
    # Example usage
    rows = fetch_expense_summary("2024-08-02","2024-08-05")
    print(rows)

    # Insert example
    #inserted = insert_expense("2024-08-21", 1999.99, "Food", "Lunch and Dinner")
    #print("Inserted:", inserted)

    # Delete example
    # deleted = delete_expense_for_date("2024-08-02")
    # print("Deleted:", deleted)
