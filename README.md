# Enterprise DSAR Compliance & SLA Workflow Engine

## ⚖️ Legal & Practical Context
Under data protection frameworks like the **EU GDPR** and India’s **Digital Data Protection Act (DPDPA)**, organizations are legally mandated to fulfill Data Subject Access Requests (DSARs) within a strict 30-day statutory window. 

In practice, many legal and compliance teams manage these workflows manually through unorganized spreadsheets or rely on ad-hoc online tools—similar to how legal professionals often use random websites for tasks like generating file hashes, rather than utilizing secure local methods (like PowerShell SHA-256 workflows). While enterprise giants use massive platforms like OneTrust, practical, lightweight workflow tracking is often missing for smaller setups.

## 🤝 The Legal Engineering Approach (Honest Collaboration)
To be fully transparent: **I am a legal professional and advocate, not a traditional software engineer.** My expertise lies in statutory comprehension, compliance risk management, and legal operations. 
* **My Role (Legal Architect & Product Owner):** I conceptualized the workflow, defined the 30-day statutory countdown rules, structured the risk-flagging logic (*On Track, At Risk, Breached*), and mapped out how privacy requests should be analyzed.
* **Technical Collaboration:** Because I am not from a pure coding background, I collaborated closely with my software engineering peers at Codefacia who helped translate these legal compliance requirements into clean, functional Python and Streamlit code. This project represents how modern legal engineering actually works: lawyers defining the compliance problem, and technical teams partnering to build the solution.

## 🛠️ Key Features of the Tool
* **Interactive Request Lookup & Auto-Fill:** Select a Request ID to instantly pull up the corresponding requester, request type, and tailored statutory purpose.
* **Automated SLA Calculations:** Programmatically computes compliance deadlines from the date of receipt against statutory windows.
* **Risk-Flagging Engine:** Instantly categorizes request statuses (*Successfully Closed*, *On Track*, *At Risk*, and *SLA Breached*).
* **Master Compliance Audit Log:** A complete tracking table with an expandable intake wizard to add new requests on the fly.

## 🚀 Live Application
You can test and interact with the live compliance engine here:
👉 https://dsar-compliance-engine-vu62b5ayhxreqpkamhgsph.streamlit.app/

---
*Bridging legal operations and technical collaboration.*
