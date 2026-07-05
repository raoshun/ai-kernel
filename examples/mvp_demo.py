"""
MVP Integration Example

This example demonstrates the core AI Kernel MVP functionality:
1. Creating tasks
2. Policy evaluation (Guardian)
3. Capability management
4. Execution
5. Audit logging
"""

from ai_kernel.executor.runner import ExecutorRegistry
from ai_kernel.kernel.core import Kernel
from ai_kernel.model.task import Task
from ai_kernel.model.execution import ExecutionState


def main():
    print("=" * 60)
    print("AI KERNEL MVP DEMONSTRATION")
    print("=" * 60)
    print()

    # Initialize kernel and executors
    kernel = Kernel()
    executor_registry = ExecutorRegistry()

    # Example 1: Simple Python execution
    print("1. SIMPLE PYTHON TASK")
    print("-" * 60)
    task1 = Task(objective='result = "Hello from AI Kernel!"')
    print(f"Task ID: {task1.id}")
    print(f"Objective: {task1.objective}")

    execution1 = kernel.submit_execution(task1)
    if execution1:
        print(f"✓ Execution authorized: {execution1.id}")
        executor_registry.execute("basic", execution1, kernel)
        print(f"State: {execution1.state.value}")
        if execution1.result:
            print(f"Result: {execution1.result}")
    else:
        print("✗ Execution denied")
    print()

    # Example 2: Python code with calculation
    print("2. CALCULATION TASK")
    print("-" * 60)
    task2 = Task(objective="x = 5 + 3")
    print(f"Task ID: {task2.id}")
    print(f"Objective: {task2.objective}")

    execution2 = kernel.submit_execution(task2)
    if execution2:
        print(f"✓ Execution authorized: {execution2.id}")
        executor_registry.execute("basic", execution2, kernel)
        print(f"State: {execution2.state.value}")
        if execution2.result:
            print(f"Result: {execution2.result}")
    else:
        print("✗ Execution denied")
    print()

    # Example 3: View audit logs
    print("3. AUDIT LOGS")
    print("-" * 60)
    audit_logs = kernel.get_audit_logs()
    print(f"Total audit entries: {len(audit_logs)}")
    for i, log in enumerate(audit_logs, 1):
        authorized_str = "✓" if log.authorized else "✗"
        print(f"{i}. [{authorized_str}] {log.action}: {log.description}")
    print()

    # Example 4: Capabilities
    print("4. CAPABILITY MANAGEMENT")
    print("-" * 60)
    from ai_kernel.capability.model import CapabilityType

    caps1 = kernel.capability_manager.get_capabilities(task1.id)
    print(f"Capabilities for Task 1: {len(caps1)}")
    for cap in caps1:
        print(f"  - {cap.type.value} (ID: {cap.id})")
    print()

    # Example 5: Execution status
    print("5. EXECUTION STATUS")
    print("-" * 60)
    for exec_id, execution in kernel.executions.items():
        print(f"Execution: {exec_id}")
        print(f"  Task: {execution.task.objective}")
        print(f"  State: {execution.state.value}")
        if execution.result:
            print(f"  Result: {execution.result}")
        if execution.error:
            print(f"  Error: {execution.error}")
    print()

    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Tasks created: {len(kernel.executions)}")
    completed = sum(
        1
        for e in kernel.executions.values()
        if e.state == ExecutionState.COMPLETED
    )
    failed = sum(
        1 for e in kernel.executions.values() if e.state == ExecutionState.FAILED
    )
    print(f"Completed: {completed}")
    print(f"Failed: {failed}")
    print(f"Audit entries: {len(audit_logs)}")
    print()
    print("✓ MVP demonstration complete!")


if __name__ == "__main__":
    main()
