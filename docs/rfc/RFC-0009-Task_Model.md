# RFC-0009 Task Model

| Status | Draft |
|---------|-------|
| Author | AI Kernel Project |
| Updated | 2026-07-05 |

## Abstract

This document defines the Task model used by the Kernel.

A Task represents an immutable objective that the Kernel attempts to accomplish.
Tasks are logical units of work and do not represent execution state.

Execution state is represented exclusively by Executions.

---

## Motivation

Separating objectives from execution enables retries, parallel execution,
distributed execution, and deterministic auditing without modifying the original
intent of a task.

---

## Specification

### Definition

A Task represents a logical objective.

A Task defines *what* should be accomplished but not *how* it is executed.

Tasks SHALL be immutable after creation.

---

### Identity

Every Task SHALL have a unique identifier.

The identifier MUST remain stable for the lifetime of the Task.

---

### Lifecycle

A Task is created once.

A Task SHALL NOT be modified after creation.

A Task MAY produce zero or more Executions.

A Task MAY be archived after completion.

---

### Relationship to Execution

Execution is the runtime realization of a Task.

A single Task MAY correspond to multiple Executions.

Examples include:

- retry
- parallel execution
- distributed execution
- speculative execution

The existence of multiple Executions SHALL NOT alter the identity of the Task.

---

### Parent-Child Tasks

A Task MAY create child Tasks.

Child Tasks represent independent objectives.

The relationship between parent and child SHALL be immutable.

Completion of child Tasks does not redefine the parent objective.

---

### Dependencies

A Task MAY depend on one or more Tasks.

The dependency model is implementation-defined.

Circular dependencies SHOULD be rejected.

---

### Metadata

A Task MAY contain implementation-defined metadata.

Metadata SHALL NOT modify Task semantics.

---

## Invariants

- A Task MUST represent exactly one logical objective.
- A Task MUST be immutable.
- A Task SHALL NOT contain execution state.
- A Task SHALL NOT contain execution history.
- A Task MAY produce multiple Executions.
- A Task identity MUST remain stable.

---

## Security Considerations

Task creation MAY require authorization.

Authorization is defined by the Capability and Policy models.

This RFC defines no security mechanism.

---

## Future Extensions

Future specifications MAY define:

- task priorities
- scheduling hints
- dependency semantics
- task expiration
- workflow composition
