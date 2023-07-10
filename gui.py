import tkinter as tk
import tkinter.messagebox as tkmsg
from whois_client import WhoisClient


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Domain Status Monitor")
        self.configure(bg=self.cget("bg"))
        self.whois_client = WhoisClient()
        self.domain_inputs = []

        # Calculate the screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate the window position
        window_width = 400
        window_height = 460
        window_x = (screen_width - window_width) // 2
        window_y = screen_height // 4

        # Set the window position and size
        self.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

        # Create GUI elements
        self.header_label = tk.Label(self, text="Domain Status Monitor", font=("Arial", 16))
        self.header_label.pack(pady=10)

        self.url_label = tk.Label(self, text="URL:", font=("Arial", 12))
        self.url_label.pack()

        self.url_entry = tk.Entry(self, font=("Arial", 12))
        self.url_entry.pack()
        self.url_entry.insert(tk.END, "google.com")

        self.duration_label = tk.Label(self, text="Duration (in hours):", font=("Arial", 12))
        self.duration_label.pack()

        self.duration_entry = tk.Entry(self, font=("Arial", 12))
        self.duration_entry.pack()
        self.duration_entry.insert(tk.END, "24")

        self.frequency_label = tk.Label(self, text="Frequency (in seconds):", font=("Arial", 12))
        self.frequency_label.pack()

        self.frequency_entry = tk.Entry(self, font=("Arial", 12))
        self.frequency_entry.pack()
        self.frequency_entry.insert(tk.END, "30")

        self.submit_button = tk.Button(self, text="Submit", font=("Arial", 12), command=self.submit_input)
        self.submit_button.pack(pady=10)

        self.input_list_label = tk.Label(self, text="Input List:", font=("Arial", 14, "bold"))
        self.input_list_label.pack(pady=10)

        self.input_listbox = tk.Listbox(self, font=("Arial", 12), width=40, height=6)
        self.input_listbox.pack()

        self.start_button = tk.Button(self, text="Start Monitoring", font=("Arial", 12), command=self.start_monitoring)
        self.start_button.pack(pady=10)

        self.quit_button = tk.Button(self, text="Quit", font=("Arial", 12), command=self.quit_application)
        self.quit_button.pack(pady=10)


    def submit_input(self):
        url = self.url_entry.get()
        duration = self.duration_entry.get()
        frequency = self.frequency_entry.get()

        if not url or not duration or not frequency:
            tkmsg.showerror("Error", "Please fill in all fields.")
            return

        if not duration.isdigit() or not frequency.isdigit():
            tkmsg.showerror("Error", "Please enter numeric values for duration and frequency.")
            return

        self.domain_inputs.append({"url": url, "duration": int(duration), "frequency": int(frequency)})
        self.input_listbox.insert(tk.END, f"URL: {url}  Duration: {duration}  Frequency: {frequency}")
        self.clear_entries()

    def clear_entries(self):
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(tk.END, "google.com")
        self.duration_entry.delete(0, tk.END)
        self.duration_entry.insert(tk.END, "24")
        self.frequency_entry.delete(0, tk.END)
        self.frequency_entry.insert(tk.END, "30")

    def start_monitoring(self):
        if not self.domain_inputs:
            tkmsg.showwarning("Warning", "No input provided. Please enter at least one domain to monitor.")
            return

        self.whois_client.start_monitoring_callback(self.domain_inputs)
        self.domain_inputs.clear()
        self.input_listbox.delete(0, tk.END)

    def quit_application(self):
        confirmed = tkmsg.askyesno("Confirmation", "Are you sure you want to quit? This will stop any running monitoring process.")
        if confirmed:
            self.whois_client.stop_monitoring_callback()
            self.destroy()