"""
CLI entry point for AI Kernel.
"""

from typing import Optional
from uuid import UUID

import typer
from rich.console import Console
from rich.table import Table

from ai_kernel.executor.runner import ExecutorRegistry
from ai_kernel.kernel.core import Kernel
from ai_kernel.model.task import Task
from ai_kernel.model.execution import ExecutionState

console = Console()

# Factory functions for lazy initialization
_kernel_instance = None
_executor_registry_instance = None

def get_kernel() -> Kernel:
    """Get the singleton Kernel instance."""
    global _kernel_instance
    if _kernel_instance is None:
        _kernel_instance = Kernel()
    return _kernel_instance

def get_executor_registry() -> ExecutorRegistry:
    """Get the singleton ExecutorRegistry instance."""
    global _executor_registry_instance
    if _executor_registry_instance is None:
        _executor_registry_instance = ExecutorRegistry()
    return _executor_registry_instance

# Backward compatibility aliases
kernel = get_kernel()
executor_registry = get_executor_registry()

app = typer.Typer(help="AI Kernel")


@app.command()
def version():
    """Print version information."""
    console.print("[bold cyan]AI Kernel MVP[/bold cyan]")
    console.print("Version: 0.1.0")


@app.command()
def run(
    objective: str = typer.Argument(..., help="Task objective to execute"),
    executor: str = typer.Option(
        "ollama",
        help="Executor to use: basic (Python code), shell (shell commands), ollama (natural language with Ollama)",
    ),
) -> None:
    """
    Submit a task for execution.

    Examples:
        ai-kernel run "print('Hello, World!')" --executor basic
        ai-kernel run "Create a block breaker game" --executor ollama
        ai-kernel run "ls -la" --executor shell
    """
    console.print(f"[blue]Submitting task:[/blue] {objective}")

    # Create task
    task = Task(objective=objective)
    console.print(f"[dim]Task ID: {task.id}[/dim]")

    # Submit to kernel
    execution = kernel.submit_execution(task)

    if execution is None:
        console.print("[red]✗ Execution denied by policy[/red]")
        return

    console.print(f"[green]✓ Execution authorized[/green]")
    console.print(f"[dim]Execution ID: {execution.id}[/dim]")

    # Execute
    try:
        console.print(f"[blue]Executing with {executor} executor...[/blue]")
        executor_registry.execute(executor, execution, kernel)

        # Display result
        if execution.state == ExecutionState.COMPLETED:
            console.print("[green]✓ Execution completed[/green]")
            if execution.result:
                console.print(f"[dim]Result:[/dim]\n{execution.result}")
        else:
            console.print("[red]✗ Execution failed[/red]")
            if execution.error:
                console.print(f"[dim]Error:[/dim]\n{execution.error}")

    except Exception as e:
        console.print(f"[red]✗ Error: {e}[/red]")


@app.command()
def status(execution_id: str = typer.Argument(..., help="Execution ID to check")) -> None:
    """Check execution status."""
    try:
        exec_uuid = UUID(execution_id)
        execution = kernel.get_execution(exec_uuid)

        if execution is None:
            console.print("[red]✗ Execution not found[/red]")
            return

        # Display execution status
        table = Table(title="Execution Status")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Execution ID", str(execution.id))
        table.add_row("Task ID", str(execution.task.id))
        table.add_row("Objective", execution.task.objective)
        table.add_row("State", execution.state.value)

        if execution.result:
            table.add_row("Result", execution.result[:100] + "..." if len(execution.result) > 100 else execution.result)

        if execution.error:
            table.add_row("Error", execution.error)

        console.print(table)

    except ValueError:
        console.print("[red]✗ Invalid execution ID[/red]")


@app.command()
def logs(
    execution_id: Optional[str] = typer.Option(
        None, help="Filter logs by execution ID"
    ),
) -> None:
    """View audit logs."""
    try:
        exec_uuid = UUID(execution_id) if execution_id else None

        audit_logs = kernel.get_audit_logs(exec_uuid)

        if not audit_logs:
            console.print("[yellow]No audit logs found[/yellow]")
            return

        table = Table(title="Audit Logs")
        table.add_column("Timestamp", style="cyan")
        table.add_column("Action", style="green")
        table.add_column("Description", style="white")
        table.add_column("Authorized", style="magenta")

        for log in audit_logs:
            status_icon = "✓" if log.authorized else "✗"
            table.add_row(
                log.timestamp.strftime("%H:%M:%S"),
                log.action,
                log.description[:50] + "..." if len(log.description) > 50 else log.description,
                status_icon,
            )

        console.print(table)

    except ValueError:
        console.print("[red]✗ Invalid execution ID[/red]")


@app.command()
def cancel(execution_id: str = typer.Argument(..., help="Execution ID to cancel")) -> None:
    """Cancel a pending or running execution."""
    try:
        exec_uuid = UUID(execution_id)
        cancelled = kernel.cancel_execution(exec_uuid)

        if not cancelled:
            console.print("[yellow]✗ Execution could not be cancelled[/yellow]")
            return

        console.print("[green]✓ Execution cancelled[/green]")

    except ValueError:
        console.print("[red]✗ Invalid execution ID[/red]")


@app.command()
def list_tasks() -> None:
    """List all executions."""
    if not kernel.executions:
        console.print("[yellow]No executions found[/yellow]")
        return

    table = Table(title="Executions")
    table.add_column("Execution ID", style="cyan")
    table.add_column("Task", style="green")
    table.add_column("State", style="magenta")

    for exec_id, execution in kernel.executions.items():
        table.add_row(
            str(exec_id)[:8] + "...",
            execution.task.objective[:30] + "..." if len(execution.task.objective) > 30 else execution.task.objective,
            execution.state.value,
        )

    console.print(table)
