# Support SOP: Employee Access Request Workflow

## 1. Purpose

Provide consistent triage and support for access requests that are delayed, incorrectly routed, rejected, or unable to progress.

## 2. Roles

- Service desk: initial triage and requestor communication
- Application support: application-specific access questions
- Platform support: workflow, form, notification, or SLA defects
- Process owner: policy and exception decisions

## 3. Daily monitoring

1. Review open and breached requests.
2. Identify approvals pending beyond the agreed threshold.
3. Confirm fulfillment tasks have an assignment group.
4. Review rejected records for recurring data-quality problems.
5. Record material incidents and notify the process owner.

## 4. Triage procedure

### Request not submitted

1. Confirm all mandatory fields are completed.
2. Reproduce the issue with synthetic test data.
3. Check browser console only in the prototype; check catalog/UI policies in the target ServiceNow configuration.
4. Record steps, expected outcome, actual outcome, and screenshot.

### Approval not generated

1. Confirm the request status and access level.
2. Confirm manager information exists.
3. For privileged access, confirm an application owner is defined.
4. Review target Flow Designer execution details.
5. Do not manually bypass required approval without documented authorization.

### Fulfillment not assigned

1. Confirm all required approvals are complete.
2. Check the application-to-assignment-group mapping.
3. Reassign only according to the support matrix.
4. Document the correction and probable cause.

### SLA at risk or breached

1. Confirm the SLA start, pause, and stop conditions.
2. Contact the current action owner.
3. Escalate according to impact and remaining time.
4. Record the cause category for trend analysis.

## 5. Communication standard

Every update should state the request number, current status, next owner, expected next step, and expected time. Avoid including sensitive access details in email.

## 6. Closure checklist

- Correct access level confirmed
- Required approvals recorded
- Fulfillment completed
- Requestor notified
- Resolution notes added
- SLA outcome recorded
- Related defect or knowledge article linked when applicable

## 7. Escalation

- Security or unauthorized access: immediately notify security and the process owner.
- Repeated routing failure: escalate to platform support.
- Policy exception: escalate to the application owner and process owner.
- Widespread outage: follow the major-incident process.
