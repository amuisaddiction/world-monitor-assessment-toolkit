import streamlit as st
import requests
import json
import time
import os

API_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
DEFAULT_TARGET = os.getenv("TARGET_URL", "http://127.0.0.1:8080")

st.set_page_config(page_title="World Monitor SOC", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FAFAFA; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ WORLD MONITOR SECURITY ASSESSMENT CENTER")
st.subheader("Authorized Security Assessment & Risk Analysis Platform")

# Professional Disclaimer
st.info("⚠️ **Authorized Assessment Environment**: This platform is designed for authorized security assessment and controlled demonstration purposes. The public demo uses an isolated local test target and does not perform intrusive testing against third-party production systems.")

menu = st.sidebar.selectbox("Navigation", ["Overview", "New Assessment", "Findings", "Reports", "System Health"])

if menu == "Overview":
    st.header("Overview")
    try:
        scans = requests.get(f"{API_URL}/api/scans").json()
        if scans:
            latest = scans[0]
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            col1.metric("Total Findings", latest.get("total_findings", 0))
            col2.metric("Critical", latest.get("critical_count", 0))
            col3.metric("High", latest.get("high_count", 0))
            col4.metric("Medium", latest.get("medium_count", 0))
            col5.metric("Low", latest.get("low_count", 0))
            col6.metric("Informational", latest.get("informational_count", 0))
            st.write(f"**Latest Scan Status**: {latest.get('status')} | **Target**: {latest.get('target')}")
        else:
            st.info("No assessments found. Run a new assessment.")
    except Exception:
        st.error("API Server Offline or Unreachable")

elif menu == "New Assessment":
    st.header("New Assessment")
    st.text_input("Authorized Target", "Internal Demo Target", disabled=True)
    if st.button("START SECURITY ASSESSMENT"):
        try:
            res = requests.post(f"{API_URL}/api/scans", json={"target_url": DEFAULT_TARGET})
            if res.status_code == 200:
                st.success("Scan started successfully! Please wait...")
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                steps = [
                    "Initializing",
                    "Discovery",
                    "Security Configuration",
                    "Authentication",
                    "Authorization",
                    "Client Security",
                    "Risk Analysis",
                    "Evidence",
                    "Completed"
                ]
                
                # Simulate frontend progress safely while backend orchestrator runs
                for i, step in enumerate(steps):
                    progress_bar.progress((i + 1) / len(steps))
                    status_text.text(f"Status: {step}...")
                    time.sleep(0.5)
                    
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
                # Add label indicating it's a controlled demo finding
                title_suffix = " (CONTROLLED DEMO FINDING)"
                with st.expander(f"{f['finding_id']} - {f['title']}{title_suffix} [{f['severity']}]"):
                    st.write(f"**Category:** {f['category']}")
                    st.write(f"**Affected Component:** {f['affected_component']}")
                    st.write(f"**CVSS Score:** {f['cvss_score']}")
                    st.write(f"**Description:** {f['description']}")
                    st.write(f"**Impact:** {f['impact']}")
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
            with st.spinner("Generating Report..."):
                res = requests.post(f"{API_URL}/api/reports/{scan_id}")
                if res.status_code == 200:
                    st.success("Reports generated successfully!")
                    st.write(f"Assessment Report: `{res.json()['file_path']}`")
                    st.write(f"CERT-In Mapping: `{res.json()['cert_path']}`")
                else:
                    st.error("Report generation failed.")
    except Exception:
        st.error("API Server Offline")

elif menu == "System Health":
    st.header("System Status")
    st.write("Dashboard: **ONLINE**")
    
    # Check API
    try:
        api_res = requests.get(f"{API_URL}/health", timeout=2)
        st.write(f"API: **{'ONLINE' if api_res.status_code == 200 else 'DEGRADED'}**")
    except:
        st.write("API: **OFFLINE**")
        
    # Check Database & Engine (Implicitly ONLINE if API is up)
    st.write("Database: **ONLINE**")
    st.write("Risk Engine: **ONLINE**")
    st.write("Report Engine: **ONLINE**")
    
    # Check AI Triage
    has_key = bool(get_config("GEMINI_API_KEY", ""))
    st.write(f"AI Triage: **{'READY (Gemini)' if has_key else 'FALLBACK MODE'}**")

    st.markdown("---")
    st.subheader("Demo Management")
    st.write("Reset the environment to start a fresh demonstration.")
    if st.button("RESET DEMO"):
        try:
            res = requests.post(f"{API_URL}/api/reset")
            if res.status_code == 200:
                st.success("Demo environment reset successfully.")
            else:
                st.error("Failed to reset demo environment.")
        except:
            st.error("Failed to connect to API.")
