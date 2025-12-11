"""
To-Do Router - API endpoints for managing to-do items.
"""

import os
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Optional

from services import lists_service


router = APIRouter(prefix="/todos", tags=["todos"])


class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = ""


class TodoUpdate(BaseModel):
    title: str
    description: Optional[str] = ""


class TodoStatusChange(BaseModel):
    status: str


def _get_user_email(request: Request) -> str:
    """Get user email from header or env var."""
    email = request.headers.get("X-Forwarded-Email") or os.getenv("MY_EMAIL")
    return email


def _row_to_dict(row) -> dict:
    """Convert a database row to a dictionary."""
    return {
        "id": row[0],
        "user_email": row[1],
        "title": row[2],
        "description": row[3],
        "status": row[4],
        "created_at": str(row[5]),
        "updated_at": str(row[6])
    }


@router.post("")
async def create_todo(request: Request, todo: TodoCreate):
    """Create a new to-do item."""
    try:
        email = _get_user_email(request)
        rows = lists_service.create_todo(email, todo.title, todo.description)
        if rows and len(rows) > 0:
            return _row_to_dict(rows[0])
        raise HTTPException(status_code=500, detail="Failed to create todo")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{todo_id}")
async def update_todo(request: Request, todo_id: int, todo: TodoUpdate):
    """Update an existing to-do item."""
    try:
        email = _get_user_email(request)
        rows = lists_service.update_todo(email, todo_id, todo.title, todo.description)
        if rows and len(rows) > 0:
            return _row_to_dict(rows[0])
        raise HTTPException(status_code=404, detail="Todo not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{todo_id}/status")
async def change_status(request: Request, todo_id: int, status_change: TodoStatusChange):
    """Change the status of a to-do item."""
    try:
        email = _get_user_email(request)
        rows = lists_service.change_status(email, todo_id, status_change.status)
        if rows and len(rows) > 0:
            return _row_to_dict(rows[0])
        raise HTTPException(status_code=404, detail="Todo not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("")
async def list_todos(request: Request, include_all: bool = False):
    """List to-do items. Use include_all=true to see deleted items."""
    try:
        email = _get_user_email(request)
        if include_all:
            rows = lists_service.list_all_todos(email)
        else:
            rows = lists_service.list_todos(email)
        return [_row_to_dict(row) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{todo_id}")
async def delete_todo(request: Request, todo_id: int):
    """Delete a to-do item (soft delete)."""
    try:
        email = _get_user_email(request)
        rows = lists_service.delete_todo(email, todo_id)
        if rows and len(rows) > 0:
            return _row_to_dict(rows[0])
        raise HTTPException(status_code=404, detail="Todo not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

