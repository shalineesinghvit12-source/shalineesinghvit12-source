# Sample Metrics and Measurement Plan

All values below are synthetic and generated from five seeded prototype records. They demonstrate calculation logic, not HUB International or production performance.

## Current prototype snapshot

| Metric | Definition | Sample value |
|---|---|---:|
| Total requests | Count of all seeded records | 5 |
| Open requests | Records not Closed Complete or Rejected | 2 |
| Closed requests | Records with Closed Complete status | 3 |
| SLA compliance | Closed within 48 hours / all closed | 67% |
| Average cycle time | Mean completion hours for closed requests | 37 hours |
| Privileged share | Privileged requests / total requests | 40% |

## Calculation details

- Closed cycle times: 22, 39, and 51 hours.
- SLA-compliant records: 22 and 39 hours.
- SLA compliance: 2 / 3 = 66.7%, displayed as 67%.
- Average cycle time: (22 + 39 + 51) / 3 = 37.3 hours, displayed as 37 hours.

## Recommended production KPIs

1. Request volume by application and department
2. Median and 90th-percentile fulfillment time
3. Approval wait time by approval group
4. SLA compliance by access level
5. Rejection rate and top rejection reason
6. Reassignment rate
7. Requests reopened after closure
8. Requestor satisfaction score

## Baseline and target method

Do not claim time savings without evidence. Collect at least four weeks of baseline email-request data, then compare the same metrics after rollout. Control for application, access level, request volume, and staffing changes.
