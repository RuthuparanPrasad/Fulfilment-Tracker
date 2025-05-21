import subprocess
import webbrowser
import time
from read_merge_sheets import main

# Run the data pipeline from read_merge_sheets.py
print("📊 Running fulfilment pipeline...")
main()
print("✅ Database updated.")

# Start Docker container if it's not running
container_name = "metabase"
result = subprocess.run(
    ["docker", "ps", "--format", "{{.Names}}"],
    capture_output=True,
    text=True
)
running_containers = result.stdout.strip().split("\n")

if container_name in running_containers:
    print("⚙️ Metabase is already running.")
else:
    print("🚀 Starting Metabase...")
    subprocess.run([
        "docker", "start", container_name
    ])
    time.sleep(5)  

# Open the dashboard
print("🌐 Opening dashboard at http://localhost:3000")
webbrowser.open("http://localhost:3000/dashboard/2-fulfilment-tracker?employer=&onboarding_status=&programme=")
