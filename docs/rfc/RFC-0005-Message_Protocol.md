# RFC-0005: Message Protocol

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

## Purpose

This RFC defines the messaging protocol used by all components of the AI Kernel.

The protocol provides a framework-independent contract for communication between the Kernel, Agents, and execution components.

Its objective is to standardize information exchange while preserving security, auditability, determinism, and extensibility.

This RFC intentionally specifies communication semantics rather than implementation details.

Implementations MAY use any transport mechanism provided that the behavior defined by this specification is preserved.

## Scope

This specification defines:

* Message contracts
* Message lifecycle
* Delivery semantics
* Correlation model
* Error propagation
* Security requirements
* Audit integration

This specification does not define:

* Network protocols
* Serialization formats
* Message brokers
* Threading models
* Framework-specific APIs

These concerns are implementation-specific.

## Design Principles

Every message exchanged within the AI Kernel SHALL satisfy the following principles.

### Explicit Intent

Every message SHALL represent exactly one explicit intent.

A message SHALL NOT implicitly request multiple unrelated operations.

### Immutable Messages

Messages SHALL be immutable after publication.

Corrections SHALL be expressed as new messages rather than modifications to existing messages.

### Framework Independence

Message semantics SHALL remain independent of any orchestration framework.

The protocol SHALL be compatible with synchronous, asynchronous, local, and distributed implementations.

### Deterministic Interpretation

Any compliant implementation SHALL derive the same meaning from the same message.

Interpretation SHALL NOT depend on language model reasoning.

### Traceability

Every message SHALL be traceable throughout its complete lifecycle.

Each message SHALL be associated with an audit trail.

### Correlation

Every message SHALL belong to exactly one execution context.

Relationships between messages SHALL be represented explicitly rather than inferred.

## Communication Model

All inter-component communication SHALL occur through the Kernel.

Direct Agent-to-Agent communication is prohibited.

The communication model is therefore:

Human → Kernel → Agent

Agent → Kernel → Agent

Agent → Kernel → Tool

Tool → Kernel → Agent

No component SHALL bypass the Kernel.

## Architectural Rationale

The Kernel acts as the sole communication authority.

This architecture enables:

* centralized policy enforcement;
* capability validation;
* audit recording;
* execution tracing;
* framework substitution.

Agents remain independent from one another.

The Kernel coordinates collaboration without creating direct trust relationships between Agents.

## Message Lifecycle

Every message SHALL progress through the following lifecycle.

Created

↓

Validated

↓

Accepted

↓

Processed

↓

Completed

or

Rejected

or

Expired

No implementation SHALL omit the validation phase.

## Message Ownership

Every message SHALL have exactly one producer.

Every message SHALL define its intended consumer.

A consumer MAY generate additional messages but SHALL NOT modify received messages.

Ownership is transferred only by creating new messages.

## Delivery Guarantees

The protocol defines logical delivery semantics only.

Implementations MAY provide:

* in-memory delivery;
* queue-based delivery;
* event streaming;
* RPC;
* IPC.

Regardless of transport, every implementation SHALL preserve message ordering within the same execution context whenever practical.

## Protocol Evolution

The protocol is designed to evolve without breaking existing implementations.

Future RFCs MAY introduce:

* additional message types;
* optional metadata;
* distributed routing;
* cryptographic authentication;
* transport-specific optimizations.

Extensions SHALL preserve backward compatibility whenever practical.

## Closing Statement

The Message Protocol defines the communication contract of the AI Kernel.

Components communicate by exchanging structured intent rather than invoking one another directly.

This separation enables security, observability, and framework independence while preserving architectural consistency.

## Message Envelope

Every message SHALL conform to a common logical envelope.

The envelope defines metadata required for routing, validation, auditing, and lifecycle management.

Implementations MAY serialize the envelope using any supported format.

Serialization SHALL NOT alter the semantics defined by this specification.

## Required Metadata

Every message SHALL include the following logical fields.

| Field                | Description                                |
| -------------------- | ------------------------------------------ |
| Message ID           | Globally unique identifier for the message |
| Message Type         | Logical message classification             |
| Protocol Version     | Message protocol version                   |
| Producer             | Component that created the message         |
| Consumer             | Intended receiving component               |
| Execution Context ID | Identifier of the execution context        |
| Task ID              | Identifier of the associated Task          |
| Timestamp            | Message creation time                      |
| Payload              | Message-specific content                   |

Additional metadata MAY be included provided it does not modify the meaning of required fields.

## Message Identity

Every message SHALL possess exactly one Message ID.

Message identifiers SHALL remain immutable throughout the message lifecycle.

Message identifiers SHALL NOT be reused.

Message identifiers SHOULD be globally unique.

## Execution Context

Every message SHALL belong to exactly one Execution Context.

An Execution Context represents the complete lifecycle required to satisfy one Goal.

All Tasks created during execution SHALL reference the originating Execution Context.

Execution Contexts SHALL NOT overlap.

## Task Association

Every operational message SHALL reference one Task.

Messages not associated with a Task SHALL explicitly declare that they are system messages.

Tasks MAY generate multiple messages.

Messages SHALL belong to only one Task.

## Producer

The Producer identifies the component responsible for creating the message.

Typical Producers include:

* Kernel
* Planner
* Policy Guardian
* Capability Manager
* Executor
* Reviewer
* Memory Manager
* Audit Logger

The Producer SHALL remain immutable.

## Consumer

The Consumer identifies the component expected to process the message.

Messages SHALL define exactly one intended Consumer.

Broadcast delivery is outside the scope of this specification.

Future RFCs MAY introduce multicast semantics.

## Timestamp

Every message SHALL contain a creation timestamp.

Implementations SHOULD use a monotonic clock for ordering whenever practical.

Clock synchronization mechanisms are implementation-specific.

## Payload

The Payload contains the information specific to the Message Type.

Payload semantics are defined by each individual message definition.

Envelope metadata SHALL remain independent from Payload contents.

## Parent Message

Messages MAY reference a Parent Message.

Parent relationships enable reconstruction of execution chains.

Parent references SHALL NOT create cycles.

## Correlation

Messages MAY participate in a Correlation Group.

Correlation Groups allow multiple related Tasks to be analyzed collectively.

Correlation SHALL NOT replace Task identity.

Correlation SHALL NOT replace Execution Context identity.

## Priority

Messages MAY include a scheduling priority.

Priority influences processing order only.

Priority SHALL NOT override Policy decisions.

Priority SHALL NOT bypass Capability validation.

Recommended logical priorities are:

* Critical
* High
* Normal
* Low
* Deferred

Scheduling algorithms remain implementation-specific.

## Message Size

Implementations SHOULD minimize message size.

Messages SHALL contain references rather than duplicating large artifacts whenever practical.

Large binary objects SHOULD be transferred through managed storage referenced by the Payload.

## Validation

Before acceptance, every message SHALL undergo validation.

Validation SHALL verify:

* required metadata;
* producer identity;
* consumer identity;
* protocol version;
* payload integrity;
* execution context consistency.

Messages failing validation SHALL be rejected.

Rejected messages SHALL NOT enter processing queues.

## Immutability

Accepted messages SHALL become immutable.

Any modification SHALL result in creation of a new message.

Implementations SHALL preserve the original message for audit purposes.

## Versioning

The Message Protocol SHALL support version evolution.

Every message SHALL declare the protocol version under which it was created.

Receivers MAY reject unsupported protocol versions.

Version negotiation is outside the scope of this specification.

## Forward Compatibility

Unknown optional metadata SHALL be ignored unless explicitly required by a newer protocol version.

Unknown required metadata SHALL cause validation failure.

This behavior enables incremental protocol evolution while preserving interoperability.

## Security Considerations

Envelope metadata SHALL NOT be trusted solely because it exists.

Producer identity, execution context, and capability references SHALL be independently verified by the Kernel before execution.

Metadata authenticity is an implementation responsibility.

## Audit Integration

Every accepted message SHALL generate an associated audit event.

Audit systems SHOULD preserve:

* Message ID
* Producer
* Consumer
* Task ID
* Execution Context ID
* Timestamp
* Processing Result

Audit correlation SHALL enable complete reconstruction of execution history.

## Closing Statement

The Message Envelope provides the common structural contract shared by every message exchanged within the AI Kernel.

By separating transport-independent metadata from message-specific payloads, the protocol enables interoperability, traceability, and long-term extensibility without constraining implementation choices.

## Message Types

Message Types define the logical intent of communication within the AI Kernel.

A Message Type specifies **what is being requested or reported**, not **which component generated the message**.

Message Types SHALL remain independent of implementation-specific Agent roles.

## Message Classification

Messages SHALL belong to exactly one of the following categories.

| Category | Purpose                                       |
| -------- | --------------------------------------------- |
| Request  | Requests an operation                         |
| Decision | Returns an authorization or evaluation result |
| Command  | Instructs execution of an approved operation  |
| Event    | Reports that something has occurred           |
| Result   | Reports the outcome of an operation           |
| Control  | Coordinates system behavior                   |

Future RFCs MAY introduce additional categories.

## Request Messages

Request Messages initiate work.

A Request SHALL describe the desired objective without prescribing implementation details.

Examples include:

* TaskRequest
* CapabilityRequest
* PolicyEvaluationRequest
* ToolInvocationRequest
* MemoryQueryRequest

A Request SHALL NOT imply authorization.

Authorization is determined independently by the Policy Engine.

## Decision Messages

Decision Messages communicate the outcome of an evaluation.

Decision Messages SHALL be deterministic.

Examples include:

* PolicyDecision
* CapabilityDecision
* ReviewDecision

Decision Messages SHALL include sufficient information to explain the outcome.

## Command Messages

Command Messages instruct another component to perform an already-authorized operation.

Commands SHALL only be issued after successful policy evaluation.

Examples include:

* ExecuteTask
* ExecuteTool
* CancelTask
* SuspendTask
* ResumeTask

Commands SHALL reference the Decision that authorized them.

## Event Messages

Events describe facts.

Events SHALL NOT request behavior.

Events SHALL describe something that has already occurred.

Examples include:

* TaskStarted
* TaskCompleted
* TaskFailed
* ToolStarted
* ToolCompleted
* CapabilityGranted
* CapabilityRevoked

Events SHALL be immutable.

## Result Messages

Result Messages communicate the outcome of completed work.

Results SHALL describe observed outcomes.

Results SHALL NOT reinterpret previous Decisions.

Examples include:

* TaskResult
* ToolResult
* ExecutionResult
* ReviewResult

Failures SHALL also be represented as Results.

## Control Messages

Control Messages coordinate system operation.

Examples include:

* Heartbeat
* Shutdown
* HealthStatus
* Synchronization
* ConfigurationReload

Control Messages SHALL NOT bypass Policy evaluation unless explicitly exempted by constitutional policy.

## Message Naming

Message names SHOULD satisfy the following guidelines.

Requests use imperative nouns.

Examples:

* TaskRequest
* MemoryQueryRequest

Commands use imperative verbs.

Examples:

* ExecuteTask
* CancelTask

Events use past tense.

Examples:

* TaskCompleted
* CapabilityGranted

Results use outcome-oriented nouns.

Examples:

* ExecutionResult
* ToolResult

Decision Messages end with "Decision".

Examples:

* PolicyDecision
* CapabilityDecision

Naming conventions SHOULD remain consistent throughout the specification.

## Semantic Consistency

A Message Type SHALL have exactly one semantic meaning.

The meaning of an existing Message Type SHALL NOT change across protocol versions.

Behavioral extensions SHALL introduce new Message Types rather than altering existing semantics.

## Idempotency

Message Types SHOULD declare whether repeated processing is safe.

Typical expectations are:

| Category | Expected Behavior      |
| -------- | ---------------------- |
| Request  | Implementation-defined |
| Decision | Idempotent             |
| Command  | Usually non-idempotent |
| Event    | Idempotent             |
| Result   | Idempotent             |
| Control  | Implementation-defined |

Implementations SHALL document any exceptions.

## Message Contracts

Each Message Type SHALL define:

* Purpose
* Producer
* Consumer
* Required Payload
* Optional Payload
* Expected Responses
* Failure Conditions
* Audit Requirements

Future RFCs SHALL define these contracts individually.

## Protocol Independence

The logical meaning of a Message Type SHALL remain independent of:

* transport protocol;
* serialization format;
* execution framework;
* programming language;
* deployment topology.

Equivalent implementations SHALL preserve identical observable behavior.

## Closing Statement

Message Types express architectural intent.

By separating intent from implementation roles, the protocol remains extensible, framework-independent, and compatible with future Agent architectures.

## Delivery Semantics

The Message Protocol defines logical delivery semantics.

It does not prescribe any specific transport mechanism or messaging infrastructure.

Implementations SHALL preserve the observable behavior defined by this specification regardless of the underlying transport.

## Acceptance

A message SHALL NOT be considered delivered until it has been accepted by the receiving component.

Acceptance requires successful validation as defined by this specification.

Messages that fail validation SHALL be rejected without processing.

Acceptance SHALL precede any execution.

## Processing

A receiving component SHALL process accepted messages according to their Message Type.

Processing SHALL occur at most once for each accepted message unless the Message Type explicitly permits repeated processing.

Implementations SHOULD detect duplicate deliveries whenever practical.

## Ordering

Messages belonging to the same Execution Context SHOULD preserve logical ordering.

Ordering between independent Execution Contexts is not required.

Implementations MAY reorder unrelated messages to improve throughput provided that observable behavior remains unchanged.

## Delivery Guarantees

The protocol defines the following logical delivery guarantees.

| Guarantee     | Description                                                                                 |
| ------------- | ------------------------------------------------------------------------------------------- |
| At-Most-Once  | A message is processed zero or one time.                                                    |
| At-Least-Once | A message may be processed more than once.                                                  |
| Exactly-Once  | A message is processed exactly one time from the perspective of observable system behavior. |

Implementations MAY choose any delivery mechanism.

Observable behavior SHALL remain compatible with this specification.

## Duplicate Messages

Duplicate message delivery MAY occur.

Receiving components SHALL determine whether duplicate processing is permissible.

Message IDs SHALL be used to identify duplicate deliveries.

When duplicate processing is not permitted, duplicate messages SHALL be discarded or merged according to implementation policy.

## Acknowledgement

Implementations MAY support explicit acknowledgements.

Acknowledgements SHALL indicate only successful acceptance.

They SHALL NOT imply successful execution.

Execution outcomes SHALL be reported using Result Messages.

## Timeouts

Every Request SHOULD define an expected completion deadline.

When a deadline expires before completion, the Request SHALL transition to the Expired state.

Timeout handling SHALL be reported as an Event.

Implementations MAY retry expired Requests when permitted by Policy.

## Retry

Retries SHALL create new Message instances.

A retried message SHALL reference the original Message ID.

Retries SHALL NOT overwrite historical audit records.

Retry policies are implementation-specific.

Policy evaluation MAY prohibit automatic retries.

## Cancellation

Cancellation SHALL be expressed using a Command Message.

Cancellation requests SHALL undergo Policy evaluation before execution.

Cancellation does not guarantee immediate termination.

Components SHALL report the final outcome using Event and Result Messages.

## Failure Propagation

Failures SHALL propagate through Result Messages.

Failure information SHOULD include:

* failure category;
* originating component;
* affected Task;
* timestamp;
* recoverability.

Failures SHALL NOT invalidate previously accepted audit records.

## Dead Letter Handling

Messages that cannot be processed MAY be transferred to a Dead Letter Queue or equivalent implementation-specific mechanism.

Dead Letter handling SHALL preserve the original Message.

Recovery actions SHALL create new Messages.

## Back Pressure

Implementations MAY delay message acceptance to protect system stability.

Back pressure mechanisms SHALL remain transparent to protocol semantics.

Delayed acceptance SHALL NOT modify Message contents.

## Flow Control

Flow control strategies are implementation-specific.

Examples include:

* bounded queues;
* scheduling priorities;
* concurrency limits;
* resource quotas.

Flow control SHALL NOT bypass Policy evaluation.

## Delivery Completion

Message delivery is considered complete when one of the following terminal states is reached:

* Completed
* Rejected
* Expired
* Cancelled

No additional processing SHALL occur after a terminal state unless a new Message is created.

## Closing Statement

Delivery semantics define how messages move through the AI Kernel.

By separating logical guarantees from transport implementation, the protocol remains portable across execution environments while preserving deterministic and auditable system behavior.

## Error Model

Errors are first-class protocol entities.

An error represents an observable outcome of protocol processing.

Errors SHALL be communicated through Messages.

Implementations SHALL NOT rely on implementation-specific exceptions as part of the protocol contract.

## Error Principles

Error handling SHALL satisfy the following principles.

* Explicit
* Deterministic
* Auditable
* Recoverable where practical
* Framework-independent

Every protocol failure SHALL produce observable evidence.

## Error Classification

Errors SHALL belong to one of the following categories.

| Category      | Description                                      |
| ------------- | ------------------------------------------------ |
| Validation    | Message failed structural or semantic validation |
| Authorization | Policy or Capability denied execution            |
| Execution     | Tool or execution component failed               |
| Resource      | Required resource unavailable                    |
| Communication | Message delivery failure                         |
| Timeout       | Deadline exceeded                                |
| Internal      | Unexpected implementation failure                |
| External      | Failure caused by an external dependency         |

Future RFCs MAY define additional categories.

## Error Representation

Every protocol error SHALL include:

* Error Category
* Error Identifier
* Human-readable Description
* Related Message ID
* Task ID
* Execution Context ID
* Timestamp

Additional diagnostic information MAY be included.

Diagnostic information SHALL NOT alter protocol semantics.

## Recoverability

Errors SHOULD declare whether recovery is possible.

Recovery classifications include:

| Classification | Description                                        |
| -------------- | -------------------------------------------------- |
| Recoverable    | Execution may continue after corrective action     |
| Retryable      | The operation may be attempted again               |
| Permanent      | Repeating the operation is not expected to succeed |
| Unknown        | Recovery characteristics cannot be determined      |

Recovery policy SHALL be determined independently from the error itself.

## Validation Errors

Validation errors SHALL terminate processing before execution.

Validation failures SHALL generate:

* a Result Message describing the failure;
* an associated audit record.

Invalid messages SHALL NOT enter execution.

## Authorization Errors

Authorization errors occur when Policy or Capability evaluation denies a request.

Authorization failures SHALL preserve complete audit history.

Authorization failures SHALL NOT be retried automatically unless explicitly permitted by Policy.

## Execution Errors

Execution errors occur after successful authorization.

Execution errors SHALL include sufficient information to determine:

* the operation attempted;
* the component involved;
* whether partial execution occurred.

Execution errors SHALL NOT imply protocol failure.

## Communication Errors

Communication errors occur when message delivery cannot be completed.

Implementations MAY retry communication failures.

Retry behavior SHALL comply with the Delivery Semantics defined by this specification.

## Timeout Errors

Timeouts SHALL be represented as explicit protocol outcomes.

Timeout expiration SHALL generate:

* an Event Message;
* a Result Message;
* an audit record.

Implementations SHALL distinguish timeout from cancellation.

## Internal Errors

Internal errors represent implementation defects or unexpected conditions.

Internal errors SHOULD expose sufficient diagnostic information for investigation.

Sensitive implementation details SHALL NOT be exposed outside trusted boundaries.

## External Errors

External systems are outside the trust boundary defined by RFC-0003.

Failures originating from external systems SHALL be identified as External Errors.

External failures SHALL NOT reduce protocol guarantees within the AI Kernel.

## Error Propagation

Errors SHALL propagate through Result Messages.

Propagation SHALL preserve:

* Message ID;
* Task ID;
* Execution Context ID;
* causal relationships.

Errors SHALL NOT invalidate previously accepted Messages.

## Error Chaining

An Error MAY reference a preceding Error.

Error chains SHALL remain acyclic.

Error chains SHOULD facilitate reconstruction of complex execution failures.

## Security Considerations

Error information SHALL be appropriate for the intended Consumer.

Diagnostic information SHALL NOT disclose:

* confidential data;
* credentials;
* cryptographic secrets;
* implementation-specific attack surfaces.

Security policies MAY require error information to be redacted.

## Audit Requirements

Every Error SHALL generate an audit record.

Audit records SHOULD include:

* error classification;
* related messages;
* affected components;
* execution outcome;
* recovery actions, if any.

Audit history SHALL remain immutable.

## Closing Statement

Errors are observable protocol outcomes rather than exceptional conditions.

By treating failures as structured messages, the AI Kernel preserves determinism, auditability, and consistent execution semantics across all implementations.

## Security Considerations

Message exchange is subject to the trust boundaries defined in RFC-0003.

Every message SHALL be treated as untrusted until successfully validated by the Kernel.

Successful delivery SHALL NOT imply successful authorization.

Successful authorization SHALL NOT imply successful execution.

Each stage of message processing SHALL perform only the responsibilities assigned to that stage.

## Authentication

Implementations SHALL provide a mechanism for identifying the Producer of each message.

The authentication mechanism is implementation-specific.

Authentication SHALL occur before message acceptance.

Unauthenticated messages SHALL be rejected.

## Integrity

Implementations SHOULD detect message corruption or unauthorized modification.

Integrity verification mechanisms MAY include:

* checksums;
* cryptographic hashes;
* digital signatures;
* authenticated transport mechanisms.

The protocol defines the requirement for integrity verification but does not prescribe a specific implementation.

## Authorization

Possession of a valid Message SHALL NOT grant authority.

Authority SHALL be established through Policy evaluation and Capability validation.

Message processing SHALL never bypass authorization.

## Confidentiality

Implementations SHOULD protect message contents according to operational requirements.

Confidentiality mechanisms MAY include:

* encrypted transport;
* encrypted storage;
* isolated execution environments;
* access-controlled message stores.

The protocol remains independent of the confidentiality mechanism selected.

## Trust Boundaries

Messages crossing a Trust Boundary SHALL undergo independent validation.

Trust SHALL NOT be inherited from previous processing stages.

Every boundary crossing SHALL be observable through audit records.

## Replay Protection

Implementations SHOULD detect replayed messages.

Replay detection MAY use:

* Message IDs;
* timestamps;
* nonces;
* protocol-specific mechanisms.

Replay handling SHALL preserve audit history.

## Audit Integrity

Audit records generated from message processing SHALL be immutable.

Audit systems SHOULD prevent unauthorized modification or deletion.

Integrity of audit data is essential to maintaining system trust.

## Future Security Extensions

Future RFCs MAY define:

* message signing;
* hardware-backed identities;
* remote attestation;
* encrypted message payloads;
* secure distributed routing.

Such extensions SHALL remain compatible with the Message Protocol defined by this specification.

## Protocol Compliance

An implementation claiming compliance with RFC-0005 SHALL satisfy all mandatory requirements defined using the terms SHALL or MUST.

Optional behavior defined using SHOULD or MAY does not affect compliance.

Compliance SHALL be evaluated based on externally observable protocol behavior rather than implementation details.

## Minimum Compliance Requirements

A compliant implementation SHALL satisfy at least the following requirements.

* Every message passes through the Kernel.
* Every message is validated before processing.
* Every accepted message becomes immutable.
* Every execution is associated with an Execution Context.
* Every Task is uniquely identifiable.
* Every authorization is evaluated through the Policy Model.
* Every privileged operation is governed by the Capability Model.
* Every message produces an auditable execution history.
* Every terminal outcome is represented explicitly.

Failure to satisfy any mandatory requirement SHALL result in non-compliance.

## Framework Compliance

Framework adapters SHALL preserve the semantics defined by this specification.

Adapters SHALL NOT redefine:

* message meaning;
* lifecycle;
* authorization model;
* trust boundaries;
* audit behavior.

Framework-specific optimizations SHALL remain transparent to protocol semantics.

## Interoperability

Independent implementations conforming to this specification SHOULD interoperate without requiring protocol-specific modifications.

Observable protocol behavior SHALL remain consistent across implementations.

## Future Evolution

This protocol is intended to evolve incrementally.

Future revisions SHOULD preserve backward compatibility whenever practical.

Breaking changes SHALL require a new protocol version.

Deprecated behavior SHOULD remain documented for migration purposes.

## Closing Statement

The Message Protocol establishes the architectural contract governing communication within the AI Kernel.

By separating communication semantics from implementation details, the protocol enables secure, auditable, deterministic, and framework-independent collaboration between all system components.

This specification serves as the foundation upon which higher-level execution, orchestration, and autonomous behavior are constructed.
