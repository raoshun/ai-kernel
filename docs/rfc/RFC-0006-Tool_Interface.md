# RFC-0006: Tool Interface

**Status:** Draft

**Version:** 0.1.0

**Author:** Project Maintainers

**Depends on:**

* CONSTITUTION.md
* RFC-0000: Terminology
* RFC-0001: System Architecture
* RFC-0002: Capability Model
* RFC-0003: Trust Model
* RFC-0004: Policy Model
* RFC-0005: Message Protocol

## Purpose

This RFC defines the abstract Tool Interface of the AI Kernel.

A Tool provides an executable capability that allows the Kernel to interact with systems outside of reasoning.

This specification intentionally abstracts over implementation technologies.

A Tool may represent:

* a local function;
* a command-line application;
* an operating system service;
* a REST API;
* an MCP server;
* a containerized application;
* a virtual machine;
* a remote execution environment.

The architectural contract remains identical regardless of implementation.

## Design Principles

Every Tool SHALL satisfy the following principles.

* Deterministic interface
* Explicit inputs
* Explicit outputs
* Observable execution
* Capability-controlled access
* Policy-governed invocation
* Auditability
* Replaceability

The Tool Interface SHALL remain independent of programming language and execution environment.

## Tool Definition

A Tool is an execution endpoint.

A Tool performs work.

A Tool does not make decisions.

A Tool does not evaluate Policy.

A Tool does not grant Capability.

A Tool SHALL execute only the operation requested through the Tool Interface.

## Tool Identity

Every Tool SHALL possess a unique Tool Identifier.

Tool Identifiers SHALL remain stable throughout the lifetime of the Tool.

Tool names SHOULD describe functionality rather than implementation.

Examples include:

* filesystem.read
* filesystem.write
* shell.execute
* git.commit
* browser.navigate
* http.request
* python.execute

Identifiers SHALL NOT encode deployment-specific information.

## Tool Metadata

Every Tool SHALL define metadata describing its behavior.

Required metadata includes:

* Tool Identifier
* Human-readable Description
* Supported Version
* Required Capabilities
* Expected Inputs
* Expected Outputs
* Failure Modes

Additional metadata MAY be defined by future RFCs.

## Tool Contract

Every Tool SHALL publish an explicit contract.

The contract SHALL define:

* accepted inputs;
* observable outputs;
* execution guarantees;
* side effects;
* failure conditions.

The contract SHALL remain stable across compatible Tool versions.

## Input Model

Inputs SHALL be explicit.

Implicit dependencies SHOULD be avoided.

Inputs MAY reference external resources.

Inputs SHALL NOT imply authorization.

Authorization SHALL be established independently through the Policy Model.

## Output Model

Outputs SHALL represent observable results.

Outputs SHALL distinguish between:

* successful completion;
* partial completion;
* failure.

Outputs SHALL NOT conceal execution failures.

## Determinism

Equivalent inputs SHOULD produce equivalent observable outputs whenever practical.

When deterministic execution is impossible, the Tool SHALL document the sources of variability.

Examples include:

* external APIs;
* system clocks;
* random number generation;
* network state.

## Side Effects

Every Tool SHALL explicitly declare whether execution may modify system state.

Typical classifications include:

* read-only;
* creates resources;
* modifies resources;
* deletes resources;
* external communication;
* irreversible operations.

Side effects SHALL be considered during Policy evaluation.

## Closing Statement

The Tool Interface separates reasoning from execution.

By abstracting implementation details behind a stable architectural contract, the AI Kernel enables secure, auditable, and replaceable interaction with arbitrary execution environments.
