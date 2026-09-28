import streamlit as st
import requests
import json
import time

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="World Monitor SOC", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FAFAFA; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ WORLD MONITOR SECURITY ASSESSMENT CENTER")
st.subheader("Authorized Security Assessment & Risk Analysis Platform")

menu = st.sidebar.selectbox("Navigation", ["Overview", "New Assessment", "Findings", "Reports", "System Health"])

if menu == "Overview":
    st.header("Overview")
    try:
        scans = requests.get(f"{API_URL}/api/scans").json()
        if scans:
            latest = scans[0]
            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric("Total Findings", latest.get("total_findings", 0))
            col2.metric("Critical", latest.get("critical_count", 0))
            col3.metric("High", latest.get("high_count", 0))
            col4.metric("Medium", latest.get("medium_count", 0))
            col5.metric("Low", latest.get("low_count", 0))
            st.write(f"Latest Scan Status: {latest.get('status')} | Target: {latest.get('target')}")
        else:
            st.info("No assessments found. Run a new assessment.")
    except Exception:
        st.error("API Server Offline")

elif menu == "New Assessment":
    st.header("New Assessment")
    target = st.text_input("Authorized Target", "http://127.0.0.1:8080")
    if st.button("START SECURITY ASSESSMENT"):
        try:
            res = requests.post(f"{API_URL}/api/scans", json={"target_url": target})
            if res.status_code == 200:
                st.success("Scan started successfully! Please wait...")
                time.sleep(3) # simulate progress wait
                st.info("Scan completed. Check Overview or Findings.")
            else:
                st.error(res.json().get("detail", "Error"))
        except Exception:
            st.error("Failed to connect to API")

elif menu == "Findings":
    st.header("Findings")
    try:
        findings = requests.get(f"{API_URL}/api/findings").json()
        if findings:
            for f in findings:
                with st.expander(f"{f['finding_id']} - {f['title']} ({f['severity']})"):
                    st.write(f"**Category:** {f['category']}")
                    st.write(f"**CVSS:** {f['cvss_score']}")
                    st.write(f"**Description:** {f['description']}")
                    st.write(f"**Remediation:** {f['remediation']}")
        else:
            st.info("No findings yet.")
    except Exception:
        st.error("API Server Offline")

elif menu == "Reports":
    st.header("Reports")
    try:
        scans = requests.get(f"{API_URL}/api/scans").json()
        scan_id = st.selectbox("Select Scan", [s['id'] for s in scans]) if scans else None
        if scan_id and st.button("Generate AI Report"):
            res = requests.post(f"{API_URL}/api/reports/{scan_id}")
            if res.status_code == 200:
                st.success("Report generated!")
                st.write(f"Saved to: {res.json()['file_path']}")
    except Exception:
        st.error("API Server Offline")

elif menu == "System Health":
    st.header("System Health")
    try:
        health = requests.get(f"{API_URL}/health").json()
        st.success(f"API: ONLINE ({health['service']})")
    except:
        st.error("API: OFFLINE")
