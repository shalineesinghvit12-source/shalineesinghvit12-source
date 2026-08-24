const STATUS = {
  MANAGER: "Pending Manager Approval",
  OWNER: "Pending Application Owner",
  FULFILL: "In Fulfillment",
  CLOSED: "Closed Complete",
  REJECTED: "Rejected"
};

const seedRequests = [
  {id:"REQ001042",employee:"Maya Patel",department:"Business Insurance",application:"Broker CRM",access:"Privileged",manager:"Alex Morgan",requiredDate:"2026-08-29",justification:"Support commercial account servicing and approved reporting.",status:STATUS.OWNER,createdHoursAgo:18,cycleHours:null},
  {id:"REQ001041",employee:"Daniel Kim",department:"Employee Benefits",application:"Benefits Analytics",access:"Standard",manager:"Priya Shah",requiredDate:"2026-08-27",justification:"Prepare aggregate benefits analysis for internal review.",status:STATUS.FULFILL,createdHoursAgo:31,cycleHours:null},
  {id:"REQ001040",employee:"Sofia Garcia",department:"Risk Services",application:"Claims Portal",access:"Read only",manager:"Noah Williams",requiredDate:"2026-08-25",justification:"Review claim status for risk-service coordination.",status:STATUS.CLOSED,createdHoursAgo:56,cycleHours:22},
  {id:"REQ001039",employee:"Jordan Lee",department:"Information Technology",application:"ServiceNow",access:"Privileged",manager:"Avery Brown",requiredDate:"2026-08-24",justification:"Support request workflow configuration and troubleshooting.",status:STATUS.CLOSED,createdHoursAgo:96,cycleHours:39},
  {id:"REQ001038",employee:"Ethan Reed",department:"Corporate Operations",application:"Power BI",access:"Standard",manager:"Taylor Smith",requiredDate:"2026-08-23",justification:"Review synthetic operational metrics and monthly trends.",status:STATUS.CLOSED,createdHoursAgo:122,cycleHours:51}
];

let requests = JSON.parse(localStorage.getItem("accessflow_requests") || "null") || seedRequests;
const rows = document.querySelector("#requestRows");
const dialog = document.querySelector("#requestDialog");
const form = document.querySelector("#requestForm");

function save(){ localStorage.setItem("accessflow_requests", JSON.stringify(requests)); }
function nextId(){return `REQ${String(1043 + requests.length - seedRequests.length).padStart(6,"0")}`;}
function isClosed(r){return [STATUS.CLOSED,STATUS.REJECTED].includes(r.status);}
function sla(r){
  const hours = r.cycleHours ?? r.createdHoursAgo;
  if (isClosed(r)) return hours <= 48 ? {label:"Met",cls:"good"}:{label:"Breached",cls:"breached"};
  if(hours > 48) return {label:"Breached",cls:"breached"};
  if(hours > 36) return {label:"At risk",cls:"risk"};
  return {label:`${48-hours}h left`,cls:"good"};
}
function statusClass(s){if(s===STATUS.CLOSED)return"closed";if(s===STATUS.REJECTED)return"rejected";if(s===STATUS.FULFILL)return"progress";return"pending";}
function actionFor(r){
  const role = document.querySelector("#roleFilter").value;
  if(r.status===STATUS.MANAGER && ["all","manager"].includes(role)) return "Approve as manager";
  if(r.status===STATUS.OWNER && ["all","owner"].includes(role)) return "Approve as owner";
  if(r.status===STATUS.FULFILL && ["all","fulfiller"].includes(role)) return "Complete fulfillment";
  return "No action";
}
function populateStatuses(){
  const filter=document.querySelector("#statusFilter");
  [...new Set(requests.map(r=>r.status))].forEach(s=>{const o=document.createElement("option");o.value=s;o.textContent=s;filter.appendChild(o)});
}
function render(){
  const q=document.querySelector("#searchInput").value.toLowerCase();
  const sf=document.querySelector("#statusFilter").value;
  const filtered=requests.filter(r=>(sf==="all"||r.status===sf)&&[r.id,r.employee,r.application,r.department].join(" ").toLowerCase().includes(q));
  rows.innerHTML=filtered.map(r=>{
    const s=sla(r), action=actionFor(r);
    return `<tr><td><strong>${r.id}</strong><small>${r.department}</small></td><td>${r.employee}<small>Manager: ${r.manager}</small></td><td>${r.application}</td><td>${r.access}</td><td><span class="status ${statusClass(r.status)}">${r.status}</span></td><td><span class="sla ${s.cls}">${s.label}</span></td><td><button class="table-action" data-id="${r.id}" ${action==="No action"?"disabled":""}>${action}</button></td></tr>`;
  }).join("");
  document.querySelector("#emptyState").hidden=filtered.length>0;
  const completed=requests.filter(r=>r.status===STATUS.CLOSED);
  document.querySelector("#metricTotal").textContent=requests.length;
  document.querySelector("#metricOpen").textContent=requests.filter(r=>!isClosed(r)).length;
  document.querySelector("#metricSla").textContent=completed.length?`${Math.round(completed.filter(r=>r.cycleHours<=48).length/completed.length*100)}%`:"0%";
  document.querySelector("#metricCycle").textContent=completed.length?`${Math.round(completed.reduce((a,r)=>a+r.cycleHours,0)/completed.length)}h`:"0h";
}
function progress(id){
  const r=requests.find(x=>x.id===id); if(!r)return;
  if(r.status===STATUS.MANAGER) r.status=r.access==="Privileged"?STATUS.OWNER:STATUS.FULFILL;
  else if(r.status===STATUS.OWNER) r.status=STATUS.FULFILL;
  else if(r.status===STATUS.FULFILL){r.status=STATUS.CLOSED;r.cycleHours=r.createdHoursAgo;}
  save();render();toast(`${r.id} moved to ${r.status}.`);
}
function toast(message){const el=document.querySelector("#toast");el.textContent=message;el.classList.add("show");setTimeout(()=>el.classList.remove("show"),2600)}

document.querySelector("#openForm").addEventListener("click",()=>dialog.showModal());
document.querySelector("#closeForm").addEventListener("click",()=>dialog.close());
document.querySelector("#cancelForm").addEventListener("click",()=>dialog.close());
document.querySelector("#searchInput").addEventListener("input",render);
document.querySelector("#statusFilter").addEventListener("change",render);
document.querySelector("#roleFilter").addEventListener("change",render);
rows.addEventListener("click",e=>{if(e.target.matches("[data-id]"))progress(e.target.dataset.id)});
form.addEventListener("submit",e=>{
  e.preventDefault();
  const d=Object.fromEntries(new FormData(form));
  requests.unshift({...d,id:nextId(),status:STATUS.MANAGER,createdHoursAgo:0,cycleHours:null});
  save();form.reset();dialog.close();render();toast("Request submitted and routed to manager approval.");
});

populateStatuses();render();
