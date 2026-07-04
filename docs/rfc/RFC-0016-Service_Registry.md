# RFC-0016 Service Registry

| Status | Draft |
|---------|-------|
| Author | AI Kernel Project |
| Updated | 2026-07-05 |

## Abstract

This document defines the Service Registry of the Kernel.

The Service Registry provides a standardized mechanism for discovering and
accessing Kernel-managed services. It establishes a common abstraction for
service registration and lookup while remaining independent of implementation.

This specification defines service discovery semantics rather than a registry
implementation.

---

## Motivation

Kernel components frequently depend on other services, including Agents,
Plugins, Memory Providers, Policies, and Capability Providers.

A standardized discovery mechanism improves interoperability while preventing
tight coupling between components.

---

## Specification

### Definition

A Service Registry maintains the association between service identities and
their corresponding implementations.

The Registry SHALL provide a consistent view of registered services within a
Kernel.

---

### Registered Services

The Registry MAY contain implementations of the following service categories:

- Agent
- Plugin
- Memory Provider
- Policy Provider
- Capability Provider
- Tool Provider

Future specifications MAY define additional service categories.

---

### Identity

Every registered service SHALL have a unique identifier within a Kernel.

Service identifiers SHALL remain stable while the service is registered.

---

### Registration

Services SHALL be explicitly registered before they become discoverable.

Registration procedures are implementation-defined.

Duplicate identifiers SHALL be rejected.

---

### Lookup

The Registry SHALL support lookup by identifier.

Implementations MAY provide additional lookup mechanisms, including:

- service category
- capabilities
- implementation-defined metadata

Lookup behavior SHALL be deterministic.

---

### Lifetime

A registered service MAY be removed.

Once removed, the service SHALL no longer be discoverable.

Removal SHALL NOT invalidate completed Executions.

The behavior of active users of a removed service is implementation-defined.

---

### Visibility

The Registry defines discoverability only.

The existence of a service SHALL NOT imply permission to use that service.

Authorization remains the responsibility of the Capability and Policy models.

---

### Extensibility

Plugins MAY register additional services.

Registration SHALL NOT modify the semantic contracts defined by the Kernel.

---

## Invariants

- Every registered service MUST have a unique identifier.
- Services MUST be registered before discovery.
- Lookup MUST be deterministic.
- Registration MUST NOT modify Kernel semantics.
- Discovery MUST NOT imply authorization.

---

## Security Considerations

The Registry provides discovery only.

Authorization decisions SHALL remain outside the Registry.

This specification defines no access control mechanism.

---

## Future Extensions

Future specifications MAY define:

- service versioning
- service aliases
- dependency injection
- service priorities
- distributed service discovery
- dynamic registration
