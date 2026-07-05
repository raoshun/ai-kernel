"""Integration test for the MVP workflow.

Tests the complete execution lifecycle:
Goal -> Planning -> Risk Assessment -> Policy Evaluation -> Capability Grant -> Execution -> Audit Logging
"""
import sys
sys.path.insert(0, '.')

from src.models.core_entities import Goal, Authority, Capability, Permission
from src.managers.planner import planner
from src.managers.policy_engine import policy_engine
from src.managers.capability_manager import capability_manager
from src.managers.task_executor import task_executor
from src.managers.audit_logger import audit_logger


def test_full_workflow():
    """Test the complete workflow from Goal to Execution."""
    
    # Step 1: Setup - Register capabilities and load policies
    print("\n" + "="*60)
    print("INTEGRATION TEST: Full Workflow")
    print("="*60)
    
    # Register capabilities
    cap_read = Capability(
        name="filesystem.read",
        description="Read files from the filesystem",
        scope="filesystem"
    )
    cap_write = Capability(
        name="filesystem.write",
        description="Write files to the filesystem",
        scope="filesystem"
    )
    capability_manager.add_capability(cap_read)
    capability_manager.add_capability(cap_write)
    
    # Load policy for test user
    test_authority = Authority(principal_id="test_user", role="USER")
    policy_engine.load_policy("test_user", [
        Permission(
            action="read",
            target_capability=cap_read,
            effect="ALLOW"
        ),
        Permission(
            action="write",
            target_capability=cap_write,
            effect="ALLOW"
        )
    ])
    
    # Step 2: Create a Goal
    goal = Goal(
        goal_id="goal_001",
        description="Prepare monthly report",
        expected_output_format="PDF",
        priority=3
    )
    print(f"\n[TEST] Created Goal: {goal.goal_id}")
    
    # Step 3: Planning
    tasks = planner.create_plan(goal)
    print(f"[TEST] Generated {len(tasks)} tasks")
    assert len(tasks) > 0, "Planner should generate at least one task"
    
    # Step 4: Risk Assessment
    risk = planner.estimate_risk(tasks)
    print(f"[TEST] Risk Assessment: {risk}")
    assert risk["risk_level"] in ["LOW", "MEDIUM", "HIGH"]
    
    # Step 5: Policy Evaluation & Capability Grant
    # For each task, check if the required capabilities are permitted
    authorized_capabilities = []
    for task in tasks:
        for cap_name in task.required_capabilities:
            cap = capability_manager.get_capability(cap_name)
            if cap and policy_engine.check_permission(test_authority, cap):
                authorized_capabilities.append(cap_name)
    
    print(f"[TEST] Authorized capabilities: {authorized_capabilities}")
    assert len(authorized_capabilities) > 0, "At least one capability should be authorized"
    
    # Step 6: Execution
    context = {
        "goal_id": goal.goal_id,
        "granted_capabilities": authorized_capabilities
    }
    
    for task in tasks:
        results = task_executor.execute_task(task, context)
        print(f"[TEST] Task {task.task_id} executed with {len(results)} steps")
    
    # Step 7: Verify Audit Logs
    records = audit_logger.get_all_records()
    print(f"\n[TEST] Total audit records: {len(records)}")
    
    print("\n" + "="*60)
    print("INTEGRATION TEST PASSED!")
    print("="*60)


if __name__ == "__main__":
    test_full_workflow()
