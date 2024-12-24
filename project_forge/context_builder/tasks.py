"""Compile the context from task execution."""

from typing import Any

from project_forge.models.task import Task, execute_task


def process_task(task: Task, running_context: dict[str, Any]) -> dict[str, Any]:
    """Execute a task and return the updated context."""
    return execute_task(task, running_context)
