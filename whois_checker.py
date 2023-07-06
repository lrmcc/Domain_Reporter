import re
import subprocess
import shutil
import sys
import datetime
import json
import os

# Check if whois is installed
if not shutil.which("whois"):
    print("Whois is not installed. Please install Whois for the script to run as intended.")
    sys.exit(1)

# Create "logs" directory if it doesn't exist
logs_dir = os.path.join(os.getcwd(), "logs")
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)
    print(f"Created 'logs' directory at {logs_dir}")

while True:
    website = input("Enter a website URL: ")

    # Regular expression pattern for validating a website URL
    pattern = r"^(https?://)?(www\.)?[a-zA-Z0-9_-]+\.[a-zA-Z]{2,}(.[a-zA-Z]{2,})?$"

    # Validate the website URL using regex
    if re.match(pattern, website):
        print("Valid website URL entered:", website)

        # Extract the domain name from the URL
        domain = re.search(r"(?:[a-zA-Z0-9_-]+\.[a-zA-Z]{2,}(?:\.[a-zA-Z]{2,})?)", website).group()

        # Execute the whois command with the domain as an argument
        process = subprocess.Popen(["whois", domain], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        if output:
            print("\nWHOIS information for", domain)
            print(output.decode("utf-8"))

            # Parse the WHOIS results to extract Domain Status
            domain_status = re.findall(r"Domain Status: (.+)", output.decode("utf-8"))
            if domain_status:
                print("\nDomain Status:", domain_status)

                # Prepare the data entry with timestamp and domain status
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                entry = {"timestamp": timestamp, "domain": domain, "status": domain_status}

                # Generate the file path for the domain's JSON file in the logs directory
                file_name = domain + ".json"
                file_path = os.path.join(logs_dir, file_name)

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
            print("Failed to retrieve WHOIS information.")

        break
    else:
        print("Invalid website URL. Please try again.")
