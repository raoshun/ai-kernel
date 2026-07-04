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

## Tool Lifecycle

Every Tool invocation SHALL follow a well-defined lifecycle.

The lifecycle ensures consistent execution, policy enforcement, and auditability across all Tool implementations.

The logical lifecycle is:

Requested

↓

Authorized

↓

Prepared

↓

Executing

↓

Completed

or

Failed

or

Cancelled

Each transition SHALL be observable.

## Tool Discovery

Tools SHALL be discoverable through a Tool Registry.

The Tool Registry SHALL provide metadata only.

Tool discovery SHALL NOT imply authorization.

A discovered Tool SHALL remain unavailable until Policy evaluation and Capability validation have completed.

## Tool Registration

Every Tool SHALL be registered before invocation.

Registration SHALL include:

* Tool Identifier;
* Tool Version;
* Interface Definition;
* Required Capabilities;
* Side Effect Classification;
* Supported Operations.

Registration SHALL NOT execute the Tool.

## Invocation

Tool invocation SHALL occur only through the Kernel.

Direct invocation by reasoning components is prohibited.

Every invocation SHALL reference:

* the originating Message ID;
* the associated Task ID;
* the Execution Context ID;
* the Decision authorizing execution.

Invocation SHALL create an audit event.

## Execution Context

A Tool executes within an isolated execution context.

Execution context isolation SHOULD prevent unintended interaction between concurrent Tool invocations.

Isolation mechanisms are implementation-specific.

Examples include:

* operating system processes;
* containers;
* virtual environments;
* sandboxed runtimes.

## Statelessness

Tools SHOULD be stateless.

Persistent state SHOULD be maintained by dedicated architectural components.

Examples include:

* Memory Architecture;
* Task Management;
* Workspace Storage.

A Tool SHALL NOT rely on hidden mutable state.

## Resource Access

Every external resource accessed by a Tool SHALL be explicitly identified.

Examples include:

* files;
* directories;
* network endpoints;
* databases;
* message queues;
* hardware devices.

Resource access SHALL be constrained by the granted Capabilities.

## Side Effect Declaration

Every Tool SHALL declare its expected side effects before execution.

Declared side effects SHOULD include:

* filesystem modification;
* network communication;
* process creation;
* package installation;
* configuration changes;
* irreversible operations.

Undeclared side effects constitute non-compliant behavior.

## Cancellation

Cancellation SHALL be cooperative whenever practical.

A Tool SHOULD terminate execution safely upon receiving a cancellation request.

If immediate termination is impossible, the Tool SHALL report its current execution state.

Cancellation SHALL generate both Event and Result Messages.

## Timeout Handling

Tools SHOULD declare an expected execution duration.

The Kernel MAY terminate execution exceeding permitted limits.

Timeout policies are determined by the Policy Model.

Timeout termination SHALL be auditable.

## Concurrency

Multiple Tool invocations MAY execute concurrently.

Concurrent execution SHALL NOT violate:

* Capability constraints;
* Policy decisions;
* resource isolation;
* audit consistency.

Concurrency control remains implementation-specific.

## Retry Behavior

Retry policies SHALL be explicitly defined.

Retries SHALL create new invocations.

Retries SHALL preserve references to previous attempts.

Automatic retries SHALL remain subject to Policy evaluation.

## Failure Reporting

Tool failures SHALL be reported using Result Messages.

Failures SHALL distinguish between:

* Tool failure;
* environmental failure;
* authorization failure;
* dependency failure.

Failure reports SHOULD support automated recovery where practical.

## Tool Replacement

Tools MAY be replaced without affecting architectural behavior.

Replacement Tools SHALL preserve:

* Tool Identifier;
* interface contract;
* observable semantics.

Implementation details MAY change.

Architectural behavior SHALL remain compatible.

## Compliance

A compliant Tool SHALL:

* expose an explicit contract;
* require explicit authorization;
* execute only requested operations;
* declare side effects;
* produce observable outcomes;
* generate audit records;
* preserve protocol semantics.

## Registry Model

The Tool Registry is the authoritative catalog of executable Tools available to the AI Kernel.

The Registry SHALL provide metadata describing each Tool.

The Registry SHALL NOT execute Tools.

The Registry SHALL NOT perform Policy evaluation.

The Registry SHALL NOT grant Capabilities.

The Registry is responsible solely for discovery and interface description.

## Registry Requirements

The Registry SHALL maintain, at minimum, the following information for each Tool:

* Tool Identifier
* Version
* Interface Definition
* Description
* Required Capabilities
* Side Effect Classification
* Supported Operations
* Compatibility Information
* Operational Status

Additional implementation-specific metadata MAY be stored.

## Tool Availability

Tool availability SHALL be explicitly represented.

Recommended availability states include:

* Registered
* Enabled
* Disabled
* Deprecated
* Unavailable

Only Enabled Tools MAY be selected for execution.

## Versioning

Every Tool SHALL declare a semantic version.

Version numbers SHALL identify interface compatibility rather than implementation revisions.

Patch releases SHOULD preserve identical observable behavior.

Minor releases MAY introduce backward-compatible functionality.

Major releases MAY introduce incompatible interface changes.

## Compatibility

Tool compatibility SHALL be evaluated independently of implementation language.

Two Tool implementations are considered compatible if they expose equivalent:

* interface contracts;
* observable behavior;
* capability requirements;
* side effect declarations;
* failure semantics.

Internal implementation differences SHALL NOT affect compatibility.

## Interface Stability

Published Tool contracts SHOULD remain stable.

Breaking changes SHALL require a new major version.

Deprecated interfaces SHOULD remain available for a migration period defined by the implementation.

## Deprecation

Deprecated Tools SHALL remain discoverable.

The Registry SHALL clearly indicate deprecation status.

New Task planning SHOULD avoid selecting deprecated Tools unless explicitly requested or required for compatibility.

Removal of deprecated Tools SHALL occur according to implementation policy.

## Tool Health

Implementations MAY monitor Tool health.

Health monitoring MAY include:

* availability;
* responsiveness;
* dependency status;
* execution success rate;
* recent failures.

Health information SHALL influence Tool selection but SHALL NOT modify Tool contracts.

## Tool Selection

The selection of a Tool is the responsibility of planning components.

The Registry SHALL NOT rank or recommend Tools.

Selection criteria MAY include:

* Capability requirements;
* Policy constraints;
* operational health;
* execution cost;
* historical reliability.

Selection algorithms are outside the scope of this specification.

## Tool Isolation

Failure of one Tool SHALL NOT compromise unrelated Tools.

Implementations SHOULD isolate Tool execution to minimize fault propagation.

Isolation mechanisms are implementation-specific.

## Tool Dependencies

A Tool MAY depend upon external software or services.

Dependencies SHOULD be declared through Tool metadata.

Hidden runtime dependencies SHOULD be avoided.

Dependency resolution is implementation-specific.

## Security Considerations

Registration in the Tool Registry SHALL NOT imply trust.

Every Tool invocation SHALL undergo independent:

* identity verification;
* Capability validation;
* Policy evaluation.

Tools SHALL execute with the minimum privileges necessary to perform the requested operation.

Implementations SHOULD support execution sandboxing where practical.

## Extension Model

The Tool Interface is designed for incremental evolution.

Future RFCs MAY introduce:

* streaming outputs;
* long-running execution sessions;
* distributed execution;
* hardware-backed Tools;
* transactional execution;
* capability negotiation.

Such extensions SHALL preserve backward compatibility whenever practical.

## Closing Statement

The Tool Interface establishes the architectural boundary between reasoning and execution.

By defining a stable, implementation-independent contract for executable capabilities, the AI Kernel enables secure, auditable, replaceable, and extensible interaction with external systems while maintaining strict separation between decision-making and execution.
