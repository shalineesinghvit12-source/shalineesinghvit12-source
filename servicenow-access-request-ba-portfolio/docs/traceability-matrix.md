# Requirements Traceability Matrix

| Business requirement | Functional behavior | User story | UAT cases | Prototype evidence |
|---|---|---|---|---|
| BR-01 Standardized intake | Validate required form variables and create ID | US-01 | UAT-01, UAT-02 | New access request dialog |
| BR-02 Manager approval | Initial route and manager decision | US-02 | UAT-03, UAT-04 | Manager role/action |
| BR-03 Privileged control | Conditional owner-approval branch | US-03 | UAT-05, UAT-06 | Privileged routing logic |
| BR-04 Fulfillment work | Route approved request to fulfillment | US-04 | UAT-07 | Fulfiller role/action |
| BR-05 Status communication | Display transition confirmation | US-02, US-04 | UAT-08 | Toast/status update simulation |
| BR-06 Operational metrics | Calculate backlog, SLA, and cycle time | US-05 | UAT-09, UAT-10 | Dashboard metric cards |
| BR-07 Auditable lifecycle | Unique ID and controlled status sequence | US-01 to US-04 | UAT-03, UAT-07 | Request table and workflow state |

## Traceability interpretation

Every Must business requirement maps to at least one user story and test. In a ServiceNow implementation, the final column would be expanded with catalog-item, flow, SLA-definition, report, update-set, and configuration-item identifiers.
