# UAT Plan and Test Cases

## Purpose

Validate that the future-state workflow satisfies agreed business requirements before target ServiceNow configuration is promoted.

## Entry criteria

- Requirements and user stories approved
- Test data prepared with no real employee information
- Prototype or development configuration available
- Critical defects from functional testing resolved

## Exit criteria

- All Must-requirement cases pass
- No severity-one or severity-two defect remains open
- Process owner accepts workflow behavior
- Support SOP and rollback approach are reviewed

## Test cases

| ID | Scenario | Test steps | Expected result | Mapped requirement | Prototype result |
|---|---|---|---|---|---|
| UAT-01 | Submit complete request | Complete every field and submit | Unique request is created in manager approval | BR-01 | Pass |
| UAT-02 | Prevent incomplete request | Leave one required field blank and submit | Browser prevents submission and identifies missing field | BR-01 | Pass |
| UAT-03 | Approve standard access | Approve a Standard request as manager | Request moves directly to fulfillment | BR-02, BR-07 | Pass |
| UAT-04 | Hold before approval | View a newly submitted request as fulfiller | Fulfillment action is unavailable | BR-02 | Pass |
| UAT-05 | Route privileged access | Approve Privileged request as manager | Request moves to application-owner approval | BR-03 | Pass |
| UAT-06 | Bypass owner for read-only | Approve Read only request as manager | Request moves directly to fulfillment | BR-03 | Pass |
| UAT-07 | Complete fulfillment | Complete a request in fulfillment | Status becomes Closed Complete and metric updates | BR-04, BR-07 | Pass |
| UAT-08 | Confirm transition | Perform an allowed workflow action | Confirmation message states new status | BR-05 | Pass |
| UAT-09 | Calculate SLA compliance | Review seeded completed records | Two of three completed requests meet 48-hour target: 67% | BR-06 | Pass |
| UAT-10 | Search and filter | Search by application, then filter by status | Only matching records display | BR-06 | Pass |

## Defect severity

- **Severity 1:** Workflow unavailable or unauthorized access granted.
- **Severity 2:** Approval routing, fulfillment, or SLA calculation is incorrect.
- **Severity 3:** Search, display, or noncritical validation issue.
- **Severity 4:** Cosmetic or documentation issue.

## Evidence note

The Prototype result column records local functional validation of the simulation. It is not evidence of testing inside a production ServiceNow environment.
