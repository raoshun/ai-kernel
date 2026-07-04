# RFC-0017 Scheduler

| Status | Draft |
|---------|-------|
| Author | AI Kernel Project |
| Updated | 2026-07-05 |

## Abstract

This document defines the Scheduler of the Kernel.

The Scheduler is responsible for coordinating the execution of Tasks by
creating and assigning Executions to appropriate Agents.

The Scheduler determines *when* and *where* work is executed. It does not define
*what* work should be performed.

---

## Motivation

The Kernel separates logical objectives from runtime execution.

Tasks represent immutable objectives, while Executions represent runtime
instances.

The Scheduler bridges these abstractions by creating Executions and assigning
them to Agents.

Separating scheduling from planning enables different scheduling strategies
without affecting Task semantics.

---

## Specification

### Definition

A Scheduler coordinates the execution of Tasks.

The Scheduler SHALL create Executions from Tasks and assign them to appropriate
Agents.

Scheduling policy is implementation-defined.

---

### Responsibilities

The Scheduler SHALL:

- observe executable Tasks
- create Executions
- assign Executions to Agents
- avoid modifying Task semantics

The Scheduler SHALL NOT:

- plan Tasks
- execute Tasks
- invoke Tools
- modify Policies
- modify Capabilities

---

### Execution Creation

A Scheduler MAY create one or more Executions for a Task.

The number of Executions is implementation-defined.

Execution creation SHALL preserve Task identity.

---

### Agent Assignment

Every Execution SHOULD be assigned to an appropriate Agent.

Agent selection MAY consider:

- Agent capabilities
- Agent availability
- implementation-defined scheduling policy

The assignment algorithm is implementation-defined.

---

### Parallelism

A Scheduler MAY create multiple concurrent Executions for a single Task.

Parallel execution SHALL NOT alter Task semantics.

Synchronization between Executions is implementation-defined.

---

### Retry

A Scheduler MAY create a new Execution when a previous Execution fails.

Retry SHALL create a new Execution.

Retry SHALL NOT modify the originating Task.

---

### Cancellation

The Scheduler MAY request cancellation of an Execution.

Cancellation behavior is implementation-defined.

Cancelling an Execution SHALL NOT modify Task semantics.

---

### Events

The Scheduler MAY emit Events describing scheduling decisions.

Typical examples include:

- Execution Created
- Execution Assigned
- Execution Cancelled

Event definitions are specified by the Kernel Event Model.

---

## Invariants

- A Scheduler MUST preserve Task semantics.
- Every Execution MUST originate from exactly one Task.
- A Scheduler MUST NOT execute Tasks directly.
- A Scheduler MUST NOT invoke Tools directly.
- Retry MUST create a new Execution.
- Parallel execution MUST preserve Task identity.

---

## Security Considerations

Scheduling decisions SHALL respect the Capability and Policy models.

Authorization remains outside the Scheduler.

---

## Future Extensions

Future specifications MAY define:

- priority scheduling
- deadline scheduling
- resource-aware scheduling
- distributed scheduling
- speculative scheduling
- execution preemption
