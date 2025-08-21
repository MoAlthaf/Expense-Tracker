import mysql.connector
from contextlib import contextmanager
from typing import Iterable, Optional, Dict, Any

@contextmanager
def get_db_cursor(commit: bool = False):
    """
    Yields a MySQL cursor. If commit=True, commits on success and rolls back on exception.
    Always closes cursor & connection.
    """
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
    except Exception:
        if commit:
            connection.rollback()
        raise
    finally:
        try:
            cursor.close()
        finally:
            connection.close()


def fetch_expenses(expense_date: Optional[str] = None) -> Iterable[Dict[str, Any]]:
    """
    Returns a list of expense rows. If expense_date is None, returns all rows.
    expense_date should be 'YYYY-MM-DD' for a DATE column.
    """
    with get_db_cursor(commit=False) as cursor:
       
        try:
            cursor.execute(
                "SELECT * FROM expenses WHERE expense_date = %s",
                (expense_date,),
            )
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        


def delete_expense_for_date(expense_date: str) -> int:
    """
    Deletes rows for a given date. Returns number of rows deleted.
    """
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "DELETE FROM expenses WHERE expense_date = %s",
            (expense_date,),
        )
        return cursor.rowcount


def insert_expense(expense_date: str, amount: float, category: str, notes: Optional[str]) -> int:
    """
    Inserts one expense. Returns number of rows inserted (1 on success).
    """
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            """
            INSERT INTO expenses (expense_date, amount, category, notes)
            VALUES (%s, %s, %s, %s)
            """,
            (expense_date, amount, category, notes),
        )
        return cursor.rowcount

def fetch_expense_summary(start_date: str, end_date: str) -> Iterable[Dict[str, Any]]:
    with get_db_cursor(commit=False) as cursor:
        cursor.execute('''SELECT category,SUM(amount) as total FROM expenses WHERE 
        expense_date BETWEEN %s and %s GROUP BY category;''',(start_date, end_date))
        return cursor.fetchall()


if __name__ == "__main__":
    # Example usage
    rows = fetch_expense_summary("2024-08-02","2024-08-05")
    print(rows)

    # Insert example
    # inserted = insert_expense("2024-08-21", 19.99, "Food", "Lunch")
    # print("Inserted:", inserted)

    # Delete example
    # deleted = delete_expense_for_date("2024-08-02")
    # print("Deleted:", deleted)
