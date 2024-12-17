from multiprocessing import Process
import subprocess
import os

def run_script(script_path):
    """Execute the given script in a separate process."""
    if os.path.exists(script_path):
        print(f"Starting execution of {script_path}")
        # Use subprocess to run the script in a separate process
        subprocess.run(["python", script_path], check=True)
    else:
        print(f"Error: Script {script_path} not found!")

if __name__ == "__main__":
    # List of Python scripts to run concurrently
    scripts = [r"c:\SPD\backend\speed_ser.py", r"c:\SPD\backend\serv_program.py"]

    # Create and start processes
    processes = []
    for script in scripts:
        process = Process(target=run_script, args=(script,))
        processes.append(process)
        process.start()

    # Wait for all processes to complete
    for process in processes:
        process.join()

    print("All scripts have finished execution.")
