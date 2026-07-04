# RFC-0011 Agent Lifecycle

| Status | Draft |
|---------|-------|
| Author | AI Kernel Project |
| Updated | 2026-07-05 |

## Abstract

This document defines the lifecycle of Agents within the Kernel.

An Agent is a long-lived Kernel component responsible for coordinating Tasks,
Executions, Memory access, Tool invocation, and Policy enforcement.

Agents are not Executions. They provide execution context rather than execution
itself.

---

## Motivation

Separating Agents from Executions enables long-lived reasoning, persistent
context, and stable coordination across multiple Tasks and Executions.

This separation also allows Kernel services such as planning, execution,
review, and governance to evolve independently.

---

## Specification

### Definition

An Agent is a long-lived Kernel component.

Agents coordinate execution but do not themselves represent executable work.

Agents MAY participate in multiple Tasks and multiple Executions during their
lifetime.

---

### Identity

Every Agent SHALL have a unique identifier.

Agent identifiers MUST remain stable throughout the lifetime of the Agent.

---

### Responsibilities

An Agent MAY perform one or more of the following responsibilities:

- planning
- execution coordination
- review
- memory access
- tool invocation
- policy evaluation

The specific responsibilities are implementation-defined.

---

### Lifecycle

An Agent SHALL exist in exactly one lifecycle state.

The standard lifecycle is:

```
Created
↓
Initializing
↓
Ready
↓
Busy
├── Idle
├── Failed
└── Stopped
```

Implementations MAY define additional internal states.

Additional states SHALL NOT alter the semantics defined by this RFC.

---

### Initialization

During initialization an Agent MAY:

- acquire resources
- initialize plugins
- establish memory access
- register capabilities

The initialization procedure is implementation-defined.

---

### Execution Coordination

An Agent MAY create, observe, suspend, resume, or terminate Executions according
to the Policy and Capability models.

Agents SHALL NOT modify Task semantics.

---

### Memory

Agents MAY query or update Memory.

Memory access SHALL be governed by the Capability and Policy models.

---

### Tool Invocation

Agents MAY invoke Tools.

Tool execution SHALL occur within the context of an Execution.

Tool invocation SHALL respect Capability constraints.

---

### Failure

Agent failure SHALL NOT invalidate existing Tasks.

Existing Executions MAY continue or be reassigned according to implementation
policy.

Recovery behavior is implementation-defined.

---

### Shutdown

An Agent MAY transition to the Stopped state.

Shutdown SHOULD release implementation-defined resources.

---

## Invariants

- An Agent MUST be long-lived.
- An Agent MUST NOT represent execution state.
- An Agent MAY coordinate multiple Tasks.
- An Agent MAY coordinate multiple Executions.
- Agents MUST NOT modify Task semantics.
- Agents MUST respect Capability and Policy constraints.

---

## Security Considerations

Agents operate within the security boundaries defined by the Capability and
Policy models.

This RFC defines no authorization mechanism.

---

## Future Extensions

Future specifications MAY define:

- distributed agents
- remote agents
- agent discovery
- agent federation
- agent migration
