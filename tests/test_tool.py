"""Test for Tool Interface (RFC-0006)."""
import sys
sys.path.insert(0, '.')

print("--- Testing Tool Interface ---")

# Test 1: Import all modules
print("\n[1] Testing imports...")
try:
    from src.ai_kernel.tool import (
        Tool,
        get_tool,
        register_tool,
        list_tools,
        get_tool_by_id,
        ToolStatus,
        SideEffectClassification,
        ToolMetadata,
        ToolContract,
        ToolInput,
        ToolOutput,
        ToolInvocation,
        ToolDefinition,
        ToolResult,
        ToolBackend,
        InMemoryToolBackend,
        get_backend,
        create_tool,
    )
    print("[PASS] All tool imports successful.")
except Exception as e:
    print(f"[FAIL] Import error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 2: Create Tool
print("\n[2] Testing tool creation...")
try:
    def sample_executor(message: str) -> str:
        return f"Echo: {message}"

    tool = create_tool(
        identifier="test.echo",
        description="Echo tool for testing",
        version="1.0.0",
        required_capabilities=["test.capability"],
        expected_inputs={"message": "string"},
        expected_outputs=["string"],
        failure_modes=["empty-input"],
        side_effects=[SideEffectClassification.READ_ONLY],
        executable=sample_executor,
    )
    assert tool.identifier == "test.echo"
    assert tool.version == "1.0.0"
    print(f"[PASS] Tool created: {tool.identifier}")
except Exception as e:
    print(f"[FAIL] Tool creation error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Register and list tools
print("\n[3] Testing registration...")
try:
    from src.ai_kernel.tool import get_tool
    tool_interface = get_tool()
    tool_interface.register_tool(tool)
    
    tools = tool_interface.list_tools()
    assert len(tools) >= 1
    print(f"[PASS] Tool registered. Total tools: {len(tools)}")
except Exception as e:
    print(f"[FAIL] Registration error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Create invocation
print("\n[4] Testing invocation creation...")
try:
    invocation = tool_interface.create_invocation(
        tool_id="test.echo",
        tool_identifier="test.echo",
        message_id="msg-001",
        task_id="task-001",
        execution_context_id="ctx-001",
        decision_id="decision-001",
    )
    assert invocation.status == ToolStatus.REQUESTED
    assert invocation.tool_identifier == "test.echo"
    print(f"[PASS] Invocation created: {invocation.id}, status: {invocation.status.value}")
except Exception as e:
    print(f"[FAIL] Invocation creation error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 5: Execute invocation
print("\n[5] Testing execution...")
try:
    output = tool_interface.execute_invocation(invocation.id, {"message": "Hello World"})
    assert output.status == ToolStatus.COMPLETED
    assert output.result == "Echo: Hello World"
    print(f"[PASS] Execution result: {output.result}")
except Exception as e:
    print(f"[FAIL] Execution error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 6: Error handling
print("\n[6] Testing error handling...")
try:
    # Create a tool that raises an exception
    def failing_executor() -> str:
        raise ValueError("Intentional error")

    failing_tool = create_tool(
        identifier="test.failing",
        description="A failing tool",
        version="1.0.0",
        required_capabilities=[],
        expected_inputs={},
        expected_outputs=[],
        failure_modes=[],
        side_effects=[SideEffectClassification.READ_ONLY],
        executable=failing_executor,
    )
    tool_interface.register_tool(failing_tool)
    
    inv = tool_interface.create_invocation(
        tool_id="test.failing",
        tool_identifier="test.failing",
    )
    output = tool_interface.execute_invocation(inv.id, {})
    
    assert output.status == ToolStatus.FAILED
    assert "Intentional error" in output.error
    print(f"[PASS] Error handling works: {output.error}")
except Exception as e:
    print(f"[FAIL] Error handling test error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 7: Tool lifecycle states
print("\n[7] Testing lifecycle transitions...")
try:
    inv2 = tool_interface.create_invocation(
        tool_id="test.echo",
        tool_identifier="test.echo",
    )
    assert inv2.status == ToolStatus.REQUESTED
    
    tool_interface.authorize_invocation(inv2.id)
    assert inv2.status == ToolStatus.AUTHORIZED
    
    tool_interface.prepare_invocation(inv2.id)
    assert inv2.status == ToolStatus.PREPARED
    
    tool_interface.cancel_invocation(inv2.id)
    assert inv2.status == ToolStatus.CANCELLED
    
    print(f"[PASS] Lifecycle transitions work correctly")
except Exception as e:
    print(f"[FAIL] Lifecycle test error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 8: List by capability
print("\n[8] Testing capability filtering...")
try:
    tools_with_cap = tool_interface.list_tools_by_capability("test.capability")
    assert len(tools_with_cap) >= 1
    print(f"[PASS] Found {len(tools_with_cap)} tool(s) with test.capability")
except Exception as e:
    print(f"[FAIL] Capability filtering error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 9: Tool metadata
print("\n[9] Testing tool metadata...")
try:
    retrieved_tool = tool_interface.get_tool("test.echo")
    assert retrieved_tool is not None
    assert retrieved_tool.metadata.identifier == "test.echo"
    assert "test.capability" in retrieved_tool.required_capabilities
    print(f"[PASS] Tool metadata retrieved: {retrieved_tool.metadata.description}")
except Exception as e:
    print(f"[FAIL] Metadata test error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 10: Unregister tool
print("\n[10] Testing unregistration...")
try:
    tool_interface.unregister_tool("test.echo")
    after_unregister = tool_interface.list_tools()
    assert not any(t.identifier == "test.echo" for t in after_unregister)
    print(f"[PASS] Tool unregistered. Remaining tools: {len(after_unregister)}")
except Exception as e:
    print(f"[FAIL] Unregistration error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 50)
print("✓ All Tool Interface tests passed!")
print("=" * 50)