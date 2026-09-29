import subprocess
import sys
import os
import time

def main():
    print("Starting World Monitor Dedicated API Service...")
    
    # 1. Start Test Target (Internal Only)
    print("Starting Internal Test Target...")
    # Passing specific host to bind internally
    env = os.environ.copy()
    target_proc = subprocess.Popen([sys.executable, "test_target/app.py"], env=env)
    
    # Wait briefly
    time.sleep(2)
    
    # 2. Start FastAPI Backend (Exposed on Render PORT)
    port = os.environ.get("PORT", "8000")
    print(f"Starting Public API Server on 0.0.0.0:{port}...")
    api_proc = subprocess.Popen([
        sys.executable, "-m", "uvicorn", "api.server:app", 
        "--host", "0.0.0.0", 
        "--port", port
    ])
    
    try:
        api_proc.wait()
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        target_proc.terminate()
        api_proc.terminate()

if __name__ == "__main__":
    main()
