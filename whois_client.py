import tkinter.messagebox as tkmsg
from thread_manager import *
from whois_parser import WhoisParser
import time


class WhoisClient():

    def __init__(self):
        self.whois_parser = WhoisParser()

    def start_monitoring_callback(self, domain_inputs):
        for domain_input in domain_inputs:
            # Start a thread for each domain retrieval
            create_thread(domain_input["url"], self.whois_parser.caller, domain_input)
        tkmsg.showinfo("Information", "Monitoring started successfully.")
    
    def stop_monitoring_callback(self):
        if len(thread_dict) != 0:
            WhoisParser.stop_event.set()
            destroy_all_threads()
            while len(thread_dict) != 0:
                time.sleep(0.1)
            tkmsg.showinfo("Information", "Monitoring stopped successfully.")