from ai_kernel.model.execution import Execution, ExecutionState
from ai_kernel.model.task import Task


def test_execution_initial_state():
    execution = Execution(Task("hello"))

    assert execution.state == ExecutionState.PENDING


def test_execution_has_unique_id():
    task = Task("hello")

    e1 = Execution(task)
    e2 = Execution(task)

    assert e1.id != e2.id


def test_execution_references_task():
    task = Task("hello")
    execution = Execution(task)

    assert execution.task is task


def test_cancel_pending_execution():
    task = Task("hello")
    execution = Execution(task)
    kernel = __import__("ai_kernel.kernel.core", fromlist=["Kernel"]).Kernel()
    kernel.executions[execution.id] = execution

    assert kernel.cancel_execution(execution.id)
    assert execution.state == ExecutionState.CANCELLED
    assert execution.error == "Execution cancelled"


def test_cancel_completed_execution_fails():
    task = Task("hello")
    execution = Execution(task)
    execution.state = ExecutionState.COMPLETED
    kernel = __import__("ai_kernel.kernel.core", fromlist=["Kernel"]).Kernel()
    kernel.executions[execution.id] = execution

    assert not kernel.cancel_execution(execution.id)
    assert execution.state == ExecutionState.COMPLETED


def test_cancel_running_execution():
    task = Task("hello")
    execution = Execution(task)
    execution.state = ExecutionState.RUNNING
    kernel = __import__("ai_kernel.kernel.core", fromlist=["Kernel"]).Kernel()
    kernel.executions[execution.id] = execution

    assert kernel.cancel_execution(execution.id)
    assert execution.state == ExecutionState.CANCELLED
