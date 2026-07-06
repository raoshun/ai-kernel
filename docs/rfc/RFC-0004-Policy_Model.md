# RFC-0004: Policy Model

**Status:** Accepted
**Version:** 1.0.0
**Author:** Project Maintainers
**Depends on:**

* `CONSTITUTION.md`
* `RFC-0000: Terminology`
* `RFC-0001: System Architecture`
* `RFC-0002: Capability Model`
* `RFC-0003: Trust Model`

## Purpose

This RFC defines the policy evaluation model of the AI Kernel.

Policies determine whether a requested operation is permitted under the current circumstances.

A Capability defines what an Agent can technically perform.

A Policy determines whether that Capability may be exercised for a specific request.

Policy evaluation is deterministic and independent from language model reasoning whenever practical.

## Design Principles

Policy evaluation SHALL satisfy the following principles.

* Deterministic
* Explicit
* Auditable
* Explainable
* Independent
* Composable
* Extensible

Policies SHALL be evaluated before every execution.

## Policy Engine

The Policy Engine evaluates execution requests.

It is the core policy evaluation subsystem used by the Policy Guardian.

Its responsibilities include:

* validating constitutional compliance;
* validating project policies;
* evaluating operational risk;
* determining required approvals;
* producing policy decisions.

The Policy Engine MAY consume risk assessments and operational risk inputs from a dedicated Risk Assessor component.

The Policy Engine SHALL NOT execute Tools.

The Policy Engine SHALL NOT grant Capabilities.

## Policy Inputs

Policy evaluation MAY consider:

* requested operation;
* requesting Agent;
* required Capabilities;
* execution context;
* user intent;
* risk level;
* resource scope;
* system state;
* audit history.

Policy evaluation SHALL NOT depend solely on prompt text.

## Decision Types

Every evaluation SHALL produce one of the following decisions.

| Decision        | Meaning                                               |
| --------------- | ----------------------------------------------------- |
| Allow           | Execution may continue                                |
| Deny            | Execution is prohibited                               |
| RequireApproval | Human approval is required                            |
| RequireReview   | Additional evaluation is required                     |
| Retry           | Evaluation should be repeated after conditions change |

Exactly one decision SHALL be produced.

## Policy Evaluation Flow

Every request follows the same evaluation process.

```text
Execution Request
        │
Constitution Validation
        │
Policy Evaluation
        │
Risk Evaluation
        │
Decision
        │
Capability Manager
        │
Execution
```

No execution SHALL bypass policy evaluation.

## Policy Categories

Policies SHOULD be organized into categories.

### Constitutional Policies

Derived directly from `CONSTITUTION.md`.

Examples include:

* legal compliance;
* protection of third parties;
* preservation of architectural integrity.

These policies have the highest priority.

### Security Policies

Examples include:

* capability validation;
* trust boundary enforcement;
* execution authorization;
* privilege limitation.

### Operational Policies

Examples include:

* workspace restrictions;
* execution time limits;
* network restrictions;
* resource quotas.

### Organizational Policies

Project-specific rules.

Examples include:

* approved repositories;
* approved package registries;
* approved execution environments.

## Policy Precedence

When policies conflict, the following order SHALL apply.

1. Constitution
2. Security Policies
3. Operational Policies
4. Organizational Policies
5. User Preferences

Higher-priority policies SHALL always prevail.

## Policy Composition

Multiple policies MAY participate in the same evaluation.

A request SHALL satisfy every applicable policy before execution proceeds.

Policy evaluation is conjunctive by default.

## Explainability

Every decision SHALL include an explanation.

Explanations SHOULD identify:

* evaluated policies;
* resulting decision;
* relevant evidence;
* required remediation when applicable.

The explanation SHALL be suitable for both human users and autonomous agents.

## Failure Handling

If policy evaluation cannot complete safely, the default decision SHALL be **Deny**.

When uncertainty cannot be resolved with sufficient confidence, execution SHALL NOT proceed automatically.

## Policy Evolution

Policies MAY evolve through human-approved updates.

Policy changes SHALL be versioned.

Changes SHALL remain compatible with the project Constitution.

Autonomous agents SHALL NOT modify constitutional or security policies without explicit human authorization.

## Audit Requirements

Every policy decision SHALL be recorded.

Audit records SHOULD contain:

* evaluated request;
* applicable policies;
* final decision;
* reasoning summary;
* timestamp;
* responsible component.

## Future Extensions

Future RFCs MAY introduce:

* policy templates;
* context-aware policies;
* distributed policy evaluation;
* cryptographic policy attestations;
* organizational policy packages.

Extensions SHALL remain compatible with this RFC.

## Closing Statement

Policies are the decision-making framework of the AI Kernel.

Capabilities define possibility.

Policies define permission.

Trust is established by consistently applying policy before every execution.
