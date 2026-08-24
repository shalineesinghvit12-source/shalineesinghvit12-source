# Business Requirements Document

## 1. Purpose

Define a standardized employee application-access request process that improves completeness, approval control, fulfillment visibility, and reporting for a hypothetical HUB International portfolio scenario.

All people, records, systems, process assumptions, and performance values in this document are synthetic. The document does not describe HUB International's actual internal environment.

## 2. Current-state problem

Requests submitted through email or chat may omit required information. Approvals are difficult to trace, privileged access may not receive consistent review, and employees must follow up manually for status. Support teams lack a reliable view of backlog, SLA risk, and cycle time.

## 3. Objectives

1. Provide one structured intake channel for application access.
2. Apply approval rules based on access risk.
3. Route approved work to the correct fulfillment team.
4. Provide requestors with status notifications.
5. Measure volume, backlog, SLA compliance, and completion time.

## 4. Scope

### In scope

- Employee access requests for five fictionalized enterprise application categories relevant to an insurance brokerage scenario
- Standard, read-only, and privileged access levels
- Manager and application-owner approvals
- IT fulfillment, notification, closure, and SLA reporting

### Out of scope

- Direct account creation in external applications
- Identity-provider integration
- Production security roles or real employee data
- License-cost optimization and access recertification

## 5. Stakeholders

| Stakeholder | Need | Responsibility |
|---|---|---|
| Employee | Simple submission and visible status | Provide complete request information |
| Manager | Confirm business need | Approve or reject each request |
| Application owner | Control privileged access | Review elevated-access requests |
| IT fulfiller | Clear and approved work | Provision access and update task |
| Service owner | Operational visibility | Monitor KPIs and improve process |
| Business Analyst | Traceable requirements | Facilitate, document, validate, and support UAT |

## 6. Business requirements

| ID | Requirement | Priority | Success measure |
|---|---|---|---|
| BR-01 | Employees must use a standardized access request form. | Must | 100% required fields completed |
| BR-02 | Every request must receive manager approval. | Must | No fulfillment before approval |
| BR-03 | Privileged requests must receive application-owner approval. | Must | 100% privileged requests receive second approval |
| BR-04 | Approved requests must create visible fulfillment work. | Must | Fulfillment stage recorded for each approved request |
| BR-05 | Requestors must be informed of material status changes. | Should | Notification event captured at approval, rejection, and closure |
| BR-06 | Service owners must see SLA and cycle-time metrics. | Must | Dashboard produces defined KPIs |
| BR-07 | The process must maintain an auditable status history. | Must | Each transition is attributable and timestamped in target design |

## 7. Non-functional requirements

- Required fields must be validated before submission.
- The request list must support search and status filtering.
- The prototype must not store confidential or production employee data.
- Target configuration should follow least-privilege access principles.
- The target workflow must support testing without changes to production records.

## 8. Assumptions and constraints

- The 48-hour SLA is a demonstration assumption, not an enterprise commitment.
- Mock users represent approval groups and fulfillers.
- IntegrationHub and external identity integrations are future enhancements.

## 9. Acceptance and sign-off

The solution is ready for stakeholder acceptance when all Must requirements map to passing UAT cases, no severity-one defects remain, and the process owner approves the future-state workflow.
