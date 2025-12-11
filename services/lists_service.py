"""
Lists Service - CRUD operations for to-do items.

**SECURITY WARNING**: THIS SERVICE USES F-STRINGS FOR SQL QUERIES INSTEAD OF 
PARAMETERIZED QUERIES. THIS IS VULNERABLE TO SQL INJECTION AND IS NOT SAFE 
FOR PRODUCTION USE. THIS IS ONLY ACCEPTABLE FOR THIS DEMO.
"""

from services.lakebase import Lakebase


def _get_table_name(user_email: str) -> str:
    """Derive table name from user email."""
    prefix = user_email.split('@')[0].replace('.', '_')
    return f"public.{prefix}_lists"


def create_todo(user_email: str, title: str, description: str):
    """Create a new to-do item."""
    email = user_email.lower()
    table = _get_table_name(email)
    sql = f"""
        INSERT INTO {table} (user_email, title, description)
        VALUES ('{email}', '{title}', '{description}')
        RETURNING *
    """
    return Lakebase.query(sql)


def update_todo(user_email: str, todo_id: int, title: str, description: str):
    """Update an existing to-do item."""
    email = user_email.lower()
    table = _get_table_name(email)
    sql = f"""
        UPDATE {table}
        SET title = '{title}', description = '{description}', updated_at = now()
        WHERE id = {todo_id} AND user_email = '{email}'
        RETURNING *
    """
    return Lakebase.query(sql)


def change_status(user_email: str, todo_id: int, status: str):
    """Change the status of a to-do item."""
    email = user_email.lower()
    table = _get_table_name(email)
    sql = f"""
        UPDATE {table}
        SET status = '{status}', updated_at = now()
        WHERE id = {todo_id} AND user_email = '{email}'
        RETURNING *
    """
    return Lakebase.query(sql)


def list_todos(user_email: str):
    """List all non-deleted to-do items for a user."""
    email = user_email.lower()
    table = _get_table_name(email)
    sql = f"""
        SELECT id, user_email, title, description, status, created_at, updated_at
        FROM {table}
        WHERE user_email = '{email}' AND status != 'deleted'
        ORDER BY created_at DESC
    """
    return Lakebase.query(sql)


def list_all_todos(user_email: str):
    """List all to-do items including deleted ones."""
    email = user_email.lower()
    table = _get_table_name(email)
    sql = f"""
        SELECT id, user_email, title, description, status, created_at, updated_at
        FROM {table}
        WHERE user_email = '{email}'
        ORDER BY created_at DESC
    """
    return Lakebase.query(sql)


def delete_todo(user_email: str, todo_id: int):
    """Soft delete a to-do item by marking it as deleted."""
    email = user_email.lower()
    table = _get_table_name(email)
    sql = f"""
        UPDATE {table}
        SET status = 'deleted', updated_at = now()
        WHERE id = {todo_id} AND user_email = '{email}'
        RETURNING *
    """
    return Lakebase.query(sql)

