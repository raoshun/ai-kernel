# RFC-0000: Terminology

**Status:** Accepted
**Version:** 1.0.0
**Author:** Project Maintainers
**Depends on:** `CONSTITUTION.md`

## 1. Purpose

This document defines the official terminology used throughout the AI Kernel project.

The objective of this RFC is to eliminate ambiguity between human developers and autonomous AI agents.

Every RFC, implementation, design discussion, issue, and pull request SHALL use the terminology defined in this document.

If a term is not defined here, its meaning should be explicitly introduced before use.

## 2. General Principles

The project distinguishes between **intent**, **authority**, **capability**, **execution**, and **policy**.

These concepts are intentionally separated.

No implementation SHALL merge them into a single abstraction.

## 3. Terminology

### Agent

An autonomous software component responsible for reasoning, planning, reviewing, or executing tasks.

An Agent may make recommendations.

An Agent does **not** inherently possess authority.

Examples:

* Planner
* Researcher
* Reviewer
* Executor

### Kernel

The trusted core of the system.

The Kernel is responsible for enforcing policy, managing capabilities, authorizing execution, coordinating workflows, and recording audit information.

The Kernel is the Root of Trust.

### Tool

A software interface capable of interacting with the external environment.

Examples include:

* Shell
* Filesystem
* Git
* Browser
* Python
* Docker
* HTTP

Tools perform actions but never make decisions.

### Function

A callable operation exposed by a Tool.

Examples:

* `read_file`
* `write_file`
* `git_commit`
* `run_python`

Functions are implementation details of Tools.

### Capability

A temporary authorization permitting an Agent to invoke a defined class of Functions.

Examples:

* filesystem.read
* filesystem.write
* shell.execute
* git.read
* browser.open

Capabilities:

* are explicit;
* are task-scoped;
* expire automatically;
* may be revoked.

Capabilities define **what an Agent may do**, not **what it should do**.

### Permission

A decision made by the Kernel allowing a requested action to proceed.

Permissions are granted after policy evaluation.

Permissions are transient.

Permissions are not equivalent to Capabilities.

A Capability enables a category of operations.

A Permission authorizes a specific operation.

### Authority

The legitimate right to make decisions within a defined scope.

Authority belongs to architectural components, not language models.

Examples:

* The Policy Guardian has authority to approve or reject execution.
* The Planner has authority to create execution plans.
* The Executor has authority to invoke approved tools.

Authority is structural and does not imply unrestricted power.

### Privilege

The effective power resulting from the combination of Authority and Capability.

The project minimizes Privilege through separation of authority and least privilege.

### Policy

A deterministic rule governing system behavior.

Policies define what is permitted, prohibited, or requires additional authorization.

Policies are enforced by the Kernel.

Policies SHALL NOT depend solely on LLM reasoning.

### Guardian

The Kernel component responsible for enforcing policies.

The Guardian evaluates execution requests and determines whether they may proceed.

The Guardian never creates execution plans.

### Task

A bounded unit of work assigned to an Agent.

A Task has:

* an objective;
* required inputs;
* expected outputs;
* completion criteria.

### Goal

A high-level objective provided by a human user or another authorized component.

A Goal may require multiple Tasks.

Example:

"Prepare the monthly report."

### Objective

A measurable outcome assigned to a Task.

Objectives should be concrete and verifiable.

Example:

"Generate report.pdf."

### Workflow

A structured sequence of Tasks required to achieve a Goal.

Workflows define ordering and dependencies but do not grant authority.

### Execution

The invocation of one or more Functions through authorized Tools.

Execution always requires:

* policy approval;
* capability validation;
* audit recording.

### Audit Record

An immutable record describing a significant system action.

Audit records should contain:

* timestamp;
* initiating component;
* objective;
* granted capabilities;
* executed functions;
* result.

### Trust Boundary

An architectural boundary across which trust assumptions change.

Every trust boundary SHALL be explicit.

Examples:

* Human → Kernel
* Kernel → Agents
* Agents → Tools
* Tools → Operating System

### Risk Level

A classification representing the potential impact of an execution.

Risk Levels are evaluated before execution.

Higher Risk Levels require stronger safeguards.

### Self-Improvement

Any modification intended to improve system behavior.

Examples include:

* prompt optimization;
* workflow refinement;
* implementation improvements;
* test generation.

Self-improvement SHALL NOT modify constitutional principles or Kernel security mechanisms without explicit human authorization.

## 4. Reserved Terms

The following words have specific meanings within this project and SHALL NOT be used interchangeably.

| Preferred Term | Do Not Substitute With |
| -------------- | ---------------------- |
| Agent          | AI, Assistant, Worker  |
| Capability     | Permission, Privilege  |
| Permission     | Capability             |
| Authority      | Permission             |
| Policy         | Prompt                 |
| Tool           | Function               |
| Goal           | Task                   |
| Objective      | Goal                   |
| Execution      | Planning               |

## 5. RFC Language

This project follows the terminology defined in RFC 2119.

The following keywords indicate requirement levels:

* **MUST** — absolute requirement.
* **MUST NOT** — absolute prohibition.
* **SHOULD** — recommended practice.
* **SHOULD NOT** — generally discouraged.
* **MAY** — optional.

These keywords are normative whenever written in uppercase.

## 6. Source of Truth

Whenever terminology conflicts arise:

1. `CONSTITUTION.md`
2. RFC-0000
3. Other RFCs
4. Implementation

Higher-priority documents SHALL prevail.

## 7. Closing Statement

Shared terminology is a prerequisite for trustworthy collaboration between humans and autonomous agents.

Clear architecture requires clear language.

Every implementation begins with a shared vocabulary.
