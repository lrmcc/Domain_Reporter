import re
import subprocess
import shutil
import sys
import datetime
import json
import os
import time
import asyncio

# Check if whois is installed
if not shutil.which("whois"):
    print("Whois is not installed. Please install Whois for the script to run as intended.")
    sys.exit(1)

# Create "logs" directory if it doesn't exist
logs_dir = os.path.join(os.getcwd(), "logs")
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)
    print(f"Created 'logs' directory at {logs_dir}")


def collect_user_input():
    while True:
        website = input("Enter a website URL (or type 'exit' to quit): ")

        if website.lower() == "exit":
            print("Exiting the script...")
            sys.exit(0)

        # Regular expression pattern for validating a website URL
        pattern = r"^(https?://)?(www\.)?[a-zA-Z0-9_-]+\.[a-zA-Z]{2,}(.[a-zA-Z]{2,})?$"

        # Validate the website URL using regex
        if re.match(pattern, website):
            print("Valid website URL entered:", website)
            return website

        print("Invalid website URL. Please try again.")


def collect_duration():
    while True:
        duration_hours = input("Enter duration (in hours, 1-96): ")
        if duration_hours.isdigit() and 1 <= int(duration_hours) <= 96:
            return int(duration_hours)
        print("Invalid duration. Please enter a whole number between 1 and 96.")


def collect_frequency():
    while True:
        frequency_seconds = input("Enter record checking frequency (in seconds, 30-3600): ")
        if frequency_seconds.isdigit() and 30 <= int(frequency_seconds) <= 3600:
            return int(frequency_seconds)
        print("Invalid frequency. Please enter a whole number between 30 and 3600.")


async def retrieve_domain_status(website, duration_hours, frequency_seconds):
    # Extract the domain name from the URL
    domain = re.search(r"(?:[a-zA-Z0-9_-]+\.[a-zA-Z]{2,}(?:\.[a-zA-Z]{2,})?)", website).group()

    # Generate the file path for the domain's JSON file in the logs directory
    file_name = domain + ".json"
    file_path = os.path.join(logs_dir, file_name)

    end_time = datetime.datetime.now() + datetime.timedelta(hours=duration_hours)

    while datetime.datetime.now() < end_time:
        # Execute the whois command with the domain as an argument
        process = subprocess.Popen(["whois", domain], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

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

        await asyncio.sleep(frequency_seconds)


async def monitor_urls():
    monitoring_tasks = []

    while True:
        website = collect_user_input()
        duration_hours = collect_duration()
        frequency_seconds = collect_frequency()

        task = asyncio.create_task(retrieve_domain_status(website, duration_hours, frequency_seconds))
        monitoring_tasks.append(task)

        choice = input("Do you want to enter another URL for monitoring? (y/n): ")
        if choice.lower() != "y":
            break

    await asyncio.gather(*monitoring_tasks)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(monitor_urls())
    loop.close()