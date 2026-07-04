# RFC-0002: Capability Model

**Status:** Accepted
**Version:** 1.0.0
**Author:** Project Maintainers
**Depends on:**

* `CONSTITUTION.md`
* `RFC-0000: Terminology`
* `RFC-0001: System Architecture`

## 1. Purpose

This RFC defines the capability-based security model of the AI Kernel.

The objective of the capability model is to ensure that every execution is authorized according to the Principle of Least Privilege while remaining transparent, auditable, and revocable.

Capabilities define what an Agent is technically allowed to do.

They do not determine what an Agent should do.

## 2. Design Principles

The capability model SHALL satisfy the following requirements.

* Least Privilege
* Explicit Authorization
* Temporary Grants
* Revocable Access
* Task Isolation
* Auditable Decisions
* Deterministic Enforcement

Capabilities SHALL NOT depend on prompt instructions.

Capabilities SHALL be enforced by the Kernel.

## 3. Security Hierarchy

The project distinguishes four different concepts.

```
Authority
        ↓
Capability
        ↓
Permission
        ↓
Execution
```

Authority determines who may make decisions.

Capability determines what classes of actions are technically available.

Permission authorizes a specific operation.

Execution invokes a Tool Function.

Each layer SHALL remain independent.

## 4. Capability Definition

A Capability SHALL contain the following attributes.

| Field       | Description                     |
| ----------- | ------------------------------- |
| Identifier  | Globally unique capability name |
| Description | Human-readable explanation      |
| Risk Level  | Relative operational risk       |
| Scope       | Accessible resources            |
| Constraints | Additional restrictions         |
| Lifetime    | Duration before expiration      |

Example:

```yaml
id: filesystem.read
description: Read files from the workspace
risk: Low
scope:
  - /workspace
constraints:
  - ReadOnly
lifetime: Task
```

## 5. Capability Categories

Capabilities SHALL be grouped into logical domains.

### Filesystem

* filesystem.read
* filesystem.write
* filesystem.delete
* filesystem.move

### Shell

* shell.execute

### Git

* git.read
* git.commit
* git.push

### Browser

* browser.open
* browser.download

### HTTP

* http.get
* http.post

### Python

* python.execute

### Docker

* docker.run
* docker.stop

Additional categories MAY be introduced through future RFCs.

## 6. Capability Lifecycle

Every Capability follows the same lifecycle.

```
Requested
      ↓
Policy Review
      ↓
Granted
      ↓
Used
      ↓
Revoked
      ↓
Archived
```

Capabilities SHALL expire automatically when the associated Task completes unless explicitly renewed by the Kernel.

## 7. Capability Grant Process

Only the Capability Manager MAY issue Capabilities.

The process SHALL be:

1. Execution request received.
2. Policy Guardian evaluates the request.
3. Capability Manager determines required capabilities.
4. Temporary capabilities are issued.
5. Executor performs the operation.
6. Capabilities are revoked.

Agents SHALL NOT self-grant capabilities.

## 8. Scope

Every Capability SHALL define its scope.

Examples include:

* directory paths;
* network destinations;
* repositories;
* containers;
* processes;
* databases.

Capabilities SHALL NOT grant unrestricted system-wide access unless explicitly approved.

## 9. Constraints

Capabilities MAY include additional constraints.

Examples:

* ReadOnly
* WorkspaceOnly
* NoNetwork
* ApprovedHostsOnly
* MaximumExecutionTime
* MaximumFileSize
* MaximumRequests

Constraints SHALL be evaluated before execution.

## 10. Risk Levels

Capabilities SHALL be classified according to operational risk.

| Level | Description              |
| ----: | ------------------------ |
|     0 | Observation              |
|     1 | Non-destructive creation |
|     2 | Modification             |
|     3 | Installation             |
|     4 | Configuration            |
|     5 | System administration    |
|     6 | Firmware                 |
|     7 | Irreversible operations  |

Higher-risk capabilities MAY require additional safeguards or explicit human approval.

## 11. Capability Composition

Multiple Capabilities MAY be granted simultaneously.

However, the combined privilege SHALL remain no greater than necessary.

The Capability Manager SHOULD avoid unnecessary combinations that increase effective privilege.

## 12. Revocation

Capabilities SHALL be revoked when:

* the Task completes;
* the Task fails;
* the user cancels execution;
* policy changes invalidate the grant;
* abnormal behavior is detected.

Revocation SHALL take precedence over execution.

## 13. Audit Requirements

Every Capability grant SHALL be recorded.

Audit records SHOULD include:

* requesting Agent;
* approving component;
* granted capabilities;
* expiration time;
* execution identifier;
* revocation reason.

## 14. Future Extensions

Future RFCs MAY define:

* hierarchical capabilities;
* delegated capabilities;
* capability inheritance;
* distributed capability management;
* cryptographic capability tokens.

Such extensions SHALL remain compatible with this RFC.

## 15. Closing Statement

Capabilities are the technical foundation of trust within the AI Kernel.

Authority decides.

Capabilities enable.

Permissions authorize.

Execution performs.


Keeping these concepts separate is essential to maintaining a secure and trustworthy autonomous system.
