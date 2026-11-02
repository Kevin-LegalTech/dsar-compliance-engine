import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
st.set_page_config(page_title="Enterprise DSAR Compliance Engine", page_icon="🛡️", layout="wide")
st.title("🛡️ Interactive Enterprise DSAR Compliance & SLA Engine")
st.markdown("An interactive legal-tech tool designed to intake, track, and analyze Data Subject Access Requests (DSARs) against **GDPR / DPDPA** statutory timelines.")
st.caption("⚖️ **Statutory & Legal Disclaimer:** All names, request IDs, and entity data utilized within this demonstration environment are entirely hypothetical mock records generated solely for illustrating DSAR compliance tracking, SLA risk evaluation, and privacy operations workflows.")

with st.expander("⚖️ About This Project & Legal Architecture (For Recruiters & Reviewers)", expanded=False):
    st.markdown("""
    ### Executive Summary & Legal Vision
    Under global privacy frameworks like the **EU GDPR** and India’s **Digital Data Protection Act (DPDPA)**, enterprises face strict statutory windows (typically 30 days) to fulfill Data Subject Access Requests (DSARs). Manually tracking these via spreadsheets creates severe regulatory risk.
    
    ### The Legal Engineering Approach (Cross-Functional Collaboration)
    * **My Role (Legal Architect & Product Owner):** As a legal professional, I conceptualized the workflow, defined the 30-day statutory countdown rules, structured the risk-flagging logic (*On Track, At Risk, Breached*), and mapped out how privacy requests should be analyzed.
    * **Technical Collaboration:** I collaborated with software engineering peers (from the Codefacia team) who helped translate these legal compliance requirements into clean Python and Streamlit code. This tool represents modern legal engineering: lawyers defining compliance needs and partnering with technical teams to build scalable solutions.
    """)

st.divider()

# Sidebar Configuration
st.sidebar.header("Statutory Parameters")
statutory_days = st.sidebar.slider("Statutory SLA Window (Days)", min_value=15, max_value=60, value=30)
warning_threshold = st.sidebar.number_input("Warning Threshold (Days Left)", value=5)

# Initialize Session State with the 5 predefined mock records
if "dsar_records" not in st.session_state:
    current_date = datetime.now().date()
    st.session_state.dsar_records = [
        {
            "Request_ID": "REQ-1001",
            "Requester_Name": "Kevin Sabu",
            "Request_Type": "Access",
            "Request_Purpose": "Full record of processing activities (RoPA) and personal data categories processed under GDPR Art. 15 / DPDPA transparency mandates.",
            "Date_Received": (current_date - timedelta(days=10)).strftime("%d-%m-%Y"),
            "Status": "Open"
        },
        {
            "Request_ID": "REQ-1002",
            "Requester_Name": "Priya Nair",
            "Request_Type": "Deletion",
            "Request_Purpose": "Exercising right to erasure ('Right to be Forgotten') regarding inactive marketing profile, telemetry logs, and user credentials.",
            "Date_Received": (current_date - timedelta(days=28)).strftime("%d-%m-%Y"),
            "Status": "Open"
        },
        {
            "Request_ID": "REQ-1003",
            "Requester_Name": "Rahul Sharma",
            "Request_Type": "Correction",
            "Request_Purpose": "Rectification of inaccurate financial transaction history and outdated residential billing records under statutory correction rights.",
            "Date_Received": (current_date - timedelta(days=35)).strftime("%d-%m-%Y"),
            "Status": "Open"
        },
        {
            "Request_ID": "REQ-1004",
            "Requester_Name": "Ananya Menon",
            "Request_Type": "Portability",
            "Request_Purpose": "Data portability request for secure, machine-readable JSON export of user-uploaded digital assets and account history.",
            "Date_Received": (current_date - timedelta(days=5)).strftime("%d-%m-%Y"),
            "Status": "Open"
        },
        {
            "Request_ID": "REQ-1005",
            "Requester_Name": "David Miller",
            "Request_Type": "Access",
            "Request_Purpose": "Completed access request regarding past customer support communications and ticketing transcripts.",
            "Date_Received": (current_date - timedelta(days=40)).strftime("%d-%m-%Y"),
            "Status": "Closed"
        }
    ]

# Function to calculate SLA deadlines and risk-flagging statuses
def process_records(records):
    processed = []
    current_date = datetime.now().date()
    
    for rec in records:
        received_date = datetime.strptime(rec["Date_Received"], "%Y-%m-%d").date()
        deadline_date = received_date + timedelta(days=statutory_days)
        days_remaining = (deadline_date - current_date).days
        
        status = rec["Status"].strip().lower()
        if status == "closed":
            sla_status = "Successfully Closed"
        elif days_remaining < 0:
            sla_status = "BREACHED (SLA Overdue)"
        elif days_remaining <= warning_threshold:
            sla_status = "At Risk (Action Required)"
        else:
            sla_status = "On Track"
            
        row = rec.copy()
        row["Deadline_Date"] = deadline_date.strftime("%Y-%m-%d")
        row["Days_Remaining"] = days_remaining
        row["SLA_Status"] = sla_status
        processed.append(row)
    return processed

# Layout Split: Request Lookup / Auto-fill Wizard on Left, Live Analysis on Right
col_form, col_report = st.columns([1, 1.2], gap="large")

with col_form:
    st.subheader("🔍 Request Lookup & Analysis Wizard")
    st.markdown("Select a Request ID to automatically retrieve the corresponding requester, statutory type, and contextual purpose.")
    
    existing_ids = [r["Request_ID"] for r in st.session_state.dsar_records]
    selected_lookup_id = st.selectbox("Select Request ID", existing_ids)
    
    matched_record = next(r for r in st.session_state.dsar_records if r["Request_ID"] == selected_lookup_id)
    
    st.text_input("Requester's Full Name (Auto-filled)", value=matched_record["Requester_Name"], disabled=True)
    st.text_input("Request Type (Auto-filled)", value=matched_record["Request_Type"], disabled=True)
    st.text_area("Request Purpose & Statutory Context (Auto-filled)", value=matched_record["Request_Purpose"], disabled=True)
    st.text_input("Date Received", value=matched_record["Date_Received"], disabled=True)
    st.text_input("Current Status", value=matched_record["Status"], disabled=True)

with col_report:
    st.subheader("📊 Live Statutory Audit & Breakdown")
    st.markdown(f"Detailed compliance evaluation for **{selected_lookup_id}**.")
    
    processed_data = process_records(st.session_state.dsar_records)
    df = pd.DataFrame(processed_data)
    
    selected_row = df[df["Request_ID"] == selected_lookup_id].iloc[0]
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Statutory SLA Window", f"{statutory_days} Days")
        st.metric("Compliance Deadline", selected_row["Deadline_Date"])
    with col_b:
        st.metric("Days Remaining", f"{selected_row['Days_Remaining']} Days")
        st.metric("Workflow Status", selected_row["Status"])
        
    st.divider()
    
    status_text = selected_row["SLA_Status"]
    if "BREACHED" in status_text:
        st.error(f"🚨 **SLA Evaluation:** {status_text}")
    elif "At Risk" in status_text:
        st.warning(f"⚠️ **SLA Evaluation:** {status_text}")
    elif "Closed" in status_text:
        st.info(f"✅ **SLA Evaluation:** {status_text}")
    else:
        st.success(f"🟢 **SLA Evaluation:** {status_text}")

st.divider()

# Master Compliance Audit Log & Add Request Feature at the bottom
st.subheader("📋 Master Compliance Audit Log")
display_columns = ["Request_ID", "Requester_Name", "Request_Type", "Request_Purpose", "Date_Received", "Deadline_Date", "Days_Remaining", "SLA_Status"]
st.dataframe(df[display_columns], use_container_width=True)

with st.expander("➕ Ingest a New DSAR Request to Pipeline"):
    with st.form("new_request_form"):
        col_x, col_y = st.columns(2)
        with col_x:
            new_id = st.text_input("Request ID", f"REQ-100{len(st.session_state.dsar_records)+1}")
            new_name = st.text_input("Requester's Full Name")
            new_type = st.selectbox("Request Type", ["Access", "Deletion", "Correction", "Portability"])
        with col_y:
            new_date = st.date_input("Date Received", datetime.now().date())
            new_status = st.selectbox("Status", ["Open", "Closed"])
            
        new_purpose = st.text_area("Request Purpose / Context", "Statutory request under GDPR / DPDPA framework.")
        
        submitted = st.form_submit_button("Submit & Append to Pipeline")
        if submitted:
            if not new_name.strip():
                st.warning("Please enter the requester's name.")
            else:
                new_entry = {
                    "Request_ID": new_id,
                    "Requester_Name": new_name,
                    "Request_Type": new_type,
                    "Request_Purpose": new_purpose,
                    "Date_Received": new_date.strftime("%Y-%m-%d"),
                    "Status": new_status
                }
                st.session_state.dsar_records.append(new_entry)
                st.success("New DSAR successfully added to the master audit log!")
                st.rerun()
