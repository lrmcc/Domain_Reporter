import datetime
import re
import json
import os
import subprocess
import time
import tkinter.messagebox as tkmsg
import threading
from whois_client import *
from file_handler import *


class WhoisParser():
    
    stop_event = threading.Event()
    
    @staticmethod
    def should_stop():
        return WhoisParser.stop_event.is_set() or WhoisParser.stop_event.wait(timeout=0)
    
    def __init__(self):
        pass
    
    def caller (self, domain_input):
        whois_caller = self.WhoisCaller(domain_input)
        end_time = datetime.datetime.now() + datetime.timedelta(hours=domain_input["duration"])
        while not WhoisParser.should_stop() and datetime.datetime.now() < end_time:
            whois_caller.call()
    

    class WhoisCaller():

        def __init__(self,domain_input):
            self.url = domain_input["url"]
            self.duration_hours = domain_input["duration"]
            self.frequency_seconds = domain_input["frequency"]
            tkmsg.showinfo("Information", (f"Retrieving {self.url} Domain Status for {self.duration_hours} hours at a {self.frequency_seconds} second frequency.\n"))
            
            self.domain = re.search(r"(?:[a-zA-Z0-9_-]+\.[a-zA-Z]{2,}(?:\.[a-zA-Z]{2,})?)", self.url).group()
            self.file_name = self.domain + ".json"

            self.logs_dir = os.path.join(os.getcwd(), "logs")
            self.file_path = os.path.join(self.logs_dir, self.file_name)

            # Get last entry, if doesn'e exist, return None
            self.domain_status = get_last_entry(self.file_path)
            
        
        def call(self):
            # Execute the whois command with the domain as an argument
            process = subprocess.Popen(["whois", self.domain], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, _ = process.communicate()

            # Check if the output is empty
            if output:
                self.get_domain_status(output)
            else:
                print(f"Failed to retrieve WHOIS information for {self.domain}.")

            # Sleep for the frequency seconds unless the stop event is set
            self.wait_for_frequency()
        
        def get_domain_status(self, output):
            # Parse the WHOIS results to extract Domain Status
            domain_status = re.findall(r"Domain Status: (.+)", output.decode("utf-8"))
            
            # Check if the domain status was found
            if not domain_status:
                print("\nDomain Status not found in WHOIS results.")

            # Check if the domain status has changed, if no change or not
            #  found, return
            if domain_status == self.domain_status or not domain_status:  
                return
            
            print(f"\nDomain Status for {self.domain}\nStatus: {domain_status}")
            append_entry(create_entry(self.domain, domain_status), self.file_path)

            # Check if the instance domain status is not None, if not, display a status change alert
            if self.domain_status != None:
                tkmsg.showwarning("Status Change","Domain Reporter has detected a change in status.")
            
            # Update the instance domain status
            self.domain_status = domain_status
        
        def wait_for_frequency(self):
            # Sleep for the frequency seconds unless the stop event is set
            temp_time = 0
            while not WhoisParser.should_stop() and temp_time < self.frequency_seconds:
                time.sleep(1)
                temp_time += 1
        
            