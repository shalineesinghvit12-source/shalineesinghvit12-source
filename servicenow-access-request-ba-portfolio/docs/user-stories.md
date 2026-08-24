# User Stories and Acceptance Criteria

## US-01: Submit a complete request

**As an employee, I want a standard application-access form so that I can provide all information needed for approval and fulfillment.**

Acceptance criteria:

1. Employee, department, application, access level, required date, manager, and justification are mandatory.
2. The request cannot be submitted when a mandatory field is empty.
3. A successful submission receives a unique request number.
4. The initial status is Pending Manager Approval.

## US-02: Manager approval

**As a manager, I want to approve or reject requests so that access is granted only when there is a valid business need.**

Acceptance criteria:

1. Every submitted request routes to manager approval.
2. Standard or read-only approval routes to fulfillment.
3. Rejection closes the request and records the rejected outcome.
4. Fulfillment cannot begin before manager approval.

## US-03: Privileged-access control

**As an application owner, I want to review privileged requests so that elevated permissions receive additional control.**

Acceptance criteria:

1. Privileged access requires application-owner approval after manager approval.
2. Standard and read-only requests bypass owner approval.
3. Owner approval routes the request to fulfillment.
4. Owner rejection closes the request as rejected.

## US-04: Fulfill approved access

**As an IT fulfiller, I want an approved work item with complete details so that I can provision the correct access.**

Acceptance criteria:

1. The fulfiller can see employee, application, access level, required date, and justification.
2. Only approved requests are available for fulfillment.
3. Completing fulfillment changes the request to Closed Complete.
4. The completion time is available for cycle-time measurement.

## US-05: Monitor service performance

**As a service owner, I want operational metrics so that I can identify delays and improve the process.**

Acceptance criteria:

1. The dashboard shows total and open requests.
2. The dashboard shows SLA compliance for completed requests.
3. The dashboard shows average cycle time for completed requests.
4. Open records show time remaining, at-risk, or breached status.

## US-06: Find and prioritize work

**As a support team member, I want search and filters so that I can quickly find requests that need action.**

Acceptance criteria:

1. Search matches request number, employee, application, or department.
2. Status filtering displays only records in the chosen state.
3. Role filtering exposes actions relevant to the chosen role.
4. A clear empty state appears when no records match.

## Definition of done

- Acceptance criteria are demonstrated.
- Mapped UAT cases pass.
- No critical accessibility or validation defect is open.
- Documentation reflects the final workflow.
- All data shown publicly is synthetic.
