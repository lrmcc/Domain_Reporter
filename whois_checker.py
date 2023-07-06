import re
import subprocess

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

            # Write the WHOIS information to a file
            with open("log.txt", "w") as file:
                file.write(output.decode("utf-8"))
                print("WHOIS information written to log.txt")

        else:
            print("Failed to retrieve WHOIS information.")

        break
    else:
        print("Invalid website URL. Please try again.")
