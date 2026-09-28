import subprocess
import sys
import time
import os

def main():
    # Setup sensible internal defaults for single-deployment mode
    os.environ["API_BASE_URL"] = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
    os.environ["TARGET_URL"] = os.getenv("TARGET_URL", "http://127.0.0.1:8080")
    
    print("Starting World Monitor Security Assessment Platform...")
    
    # 1. Start Test Target
    print("Starting Test Target on port 8080...")
    target_proc = subprocess.Popen([sys.executable, "test_target/app.py"])
    
    # 2. Start FastAPI Backend
    print("Starting API Server on port 8000...")
    api_proc = subprocess.Popen([sys.executable, "-m", "uvicorn", "api.server:app", "--host", "0.0.0.0", "--port", "8000"])
    
    # Wait for internal services to bind
    time.sleep(3)
    
    # 3. Start Streamlit Dashboard
    print("Starting Streamlit Dashboard...")
    port = os.environ.get("PORT", "8501")
    ui_proc = subprocess.Popen([
        sys.executable, "-m", "streamlit", "run", "dashboard/app.py",
        "--server.port", port,
        "--server.address", "0.0.0.0"
    ])
    
    try:
        ui_proc.wait()
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        target_proc.terminate()
        api_proc.terminate()
        ui_proc.terminate()

if __name__ == "__main__":
    main()
