import re
import subprocess
import datetime
import json
import os
import tkinter.messagebox as tkmsg
import threading
from thread_manager import ThreadManager
import time


def get_domain_status(domain_input):
        url = domain_input["url"]
        duration_hours = domain_input["duration"]
        frequency_seconds = domain_input["frequency"]
        tkmsg.showinfo("Information", (f"Retrieving {url} Domain Status for {duration_hours} hours at a {frequency_seconds} second frequency.\n"))
        # Extract the domain name from the URL
        domain = re.search(r"(?:[a-zA-Z0-9_-]+\.[a-zA-Z]{2,}(?:\.[a-zA-Z]{2,})?)", url).group()

        # Generate the file path for the domain's JSON file in the logs directory
        logs_dir = os.path.join(os.getcwd(), "logs")
        file_name = domain + ".json"
        file_path = os.path.join(logs_dir, file_name) 
        end_time = datetime.datetime.now() + datetime.timedelta(hours=duration_hours)

        while not WhoisClient.should_stop() and datetime.datetime.now() < end_time:
            # Execute the whois command with the domain as an argument
            process = subprocess.Popen(["whois", domain], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, _ = process.communicate()

            if output:
                # Parse the WHOIS results to extract Domain Status
                domain_status = re.findall(r"Domain Status: (.+)", output.decode("utf-8"))
                if domain_status:
                    print("\nDomain Status for", domain)
                    print("Status:", domain_status)

                    # Prepare the data entry with timestamp and domain status
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    entry = {"timestamp": timestamp, "domain": domain, "status": domain_status}

                    # Load existing data from the JSON file, if it exists
                    try:
                        with open(file_path, "r") as file:
                            data = json.load(file)
                    except FileNotFoundError:
                        data = []

                    # Append the new entry to the existing data
                    data.append(entry)

                    # Write the updated data to the JSON file
                    with open(file_path, "w") as file:
                        json.dump(data, file, indent=4)
                        print(f"Domain Status appended to {file_path}")

                else:
                    print("\nDomain Status not found in WHOIS results.")

            else:
                print(f"Failed to retrieve WHOIS information for {domain}.")

            temp_time = 0
            while not WhoisClient.should_stop() and temp_time < frequency_seconds:
                time.sleep(1)
                temp_time += 1

def monitor_domains(domain_inputs):
        for domain_input in domain_inputs:
            # Start a thread for each domain retrieval
            ThreadManager.create_thread(domain_input["url"], get_domain_status, domain_input)


class WhoisClient():
    stop_event = threading.Event()
    
    @staticmethod
    def should_stop():
        return WhoisClient.stop_event.is_set() or WhoisClient.stop_event.wait(timeout=0)

    def __init__(self):
        pass

    def start_monitoring_callback(self, domain_inputs):
        monitor_domains(domain_inputs)
        tkmsg.showinfo("Information", "Monitoring started successfully.")
    
    def stop_monitoring_callback(self):
        if len(ThreadManager.thread_dict) != 0:
            WhoisClient.stop_event.set()
            ThreadManager.destroy_all_threads()
            while len(ThreadManager.thread_dict) != 0:
                time.sleep(0.1)
            tkmsg.showinfo("Information", "Monitoring stopped successfully.")
        
       

