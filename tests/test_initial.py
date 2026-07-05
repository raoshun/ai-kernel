"""Minimal MVP Test to verify basic import and initialization."""
import sys
sys.path.insert(0, '.')

# Test imports
print("--- Testing Imports ---")
try:
    from src.models.core_entities import Goal, Task, Capability, Authority, Permission
    print("[PASS] Core entities imported.")
except Exception as e:
    print(f"[FAIL] Import core_entities error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    from src.managers.capability_manager import capability_manager
    print("[PASS] CapabilityManager imported.")
except Exception as e:
    print(f"[FAIL] Import capability_manager error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    from src.managers.policy_engine import policy_engine
    print("[PASS] PolicyEngine imported.")
except Exception as e:
    print(f"[FAIL] Import policy_engine error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test singleton behavior
print("\n--- Testing Singleton Behavior ---")
cap1 = capability_manager
cap2 = capability_manager
print(f"Singleton check: {cap1 is cap2}")

# Test basic Policy Engine behavior
print("\n--- Testing Policy Engine ---")
auth_test = Authority(principal_id="test_user", role="ADMIN")
print(f"Created test Authority: {auth_test}")
print("--- Initialization Complete ---")
