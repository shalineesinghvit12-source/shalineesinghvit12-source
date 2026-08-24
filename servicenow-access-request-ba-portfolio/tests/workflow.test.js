const assert = require("node:assert/strict");

function nextStatus(current, access){
  if(current === "Pending Manager Approval") return access === "Privileged" ? "Pending Application Owner" : "In Fulfillment";
  if(current === "Pending Application Owner") return "In Fulfillment";
  if(current === "In Fulfillment") return "Closed Complete";
  return current;
}

assert.equal(nextStatus("Pending Manager Approval", "Standard"), "In Fulfillment");
assert.equal(nextStatus("Pending Manager Approval", "Privileged"), "Pending Application Owner");
assert.equal(nextStatus("Pending Application Owner", "Privileged"), "In Fulfillment");
assert.equal(nextStatus("In Fulfillment", "Standard"), "Closed Complete");
console.log("Workflow routing tests passed.");
