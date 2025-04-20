import csv
import requests
import time
import os
import logging 

# Constants
PAGERDUTY_API_URL = "https://api.pagerduty.com/services"

PAGERDUTY_API_TOKEN = "u+J6aFJpC3gajNxn5_Ag" # Insert your valid API token number
DEFAULT_ESCALATION_POLICY_ID = "PDYH0SR" # Fill with your account's default escalation policy ID

if not PAGERDUTY_API_TOKEN.strip():
    print("Error: PAGERDUTY_API_TOKEN is missing. Please provide a valid API token.")
    exit(1)

if not DEFAULT_ESCALATION_POLICY_ID.strip():
    print("Error: DEFAULT_ESCALATION_POLICY_ID  is missing. Please provide a valid ID.")
    exit(1)

HEADERS = {
    "Authorization": f"Token token={PAGERDUTY_API_TOKEN}",
    "Accept": "application/vnd.pagerduty+json;version=2",
    "Content-Type": "application/json"
}

logging.basicConfig(filename="service_creation.log", level=logging.INFO, format="%(asctime)s - %(levelnames)s - %(message)s")

def create_service(service_data):
    """
    Creates a service in PagerDuty using the provided data.
    """
    while True:
        try:
            response = requests.post(PAGERDUTY_API_URL, headers=HEADERS, json=service_data)
            if response.status_code == 201:
                success_message = f"Service '{service_data['service']['name']}' created successfully."
                print(success_message)
                logging.info(success_message)
                return
            elif response.status_code == 429:
                retry_after = int(response.headers.get("Retry-After", 5))
                warning_message = f"Rate limit hit. Retrying in {retry_after} seconds..."
                print(warning_message)
                logging.warning(warning_message)
                time.sleep(retry_after)
            else:
                error_message = f"Failed to create service '{service_data['service']['name']}': {response.status_code} - {response.text}"
                print(error_message)
                logging.error(error_message)
                return
        except Exception as e:
            print(f"Error creating service '{service_data['service']['name']}': {str(e)}")

def read_csv_and_create_services(csv_file_path):
    """
    Reads a CSV file and creates services in PagerDuty for each row.
    """

    if not os.path.exists(csv_file_path):
        print(f"Error: CSV file '{csv_file_path}' not found.")
        exit(1)
    try:
        with open(csv_file_path, mode='r') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                if row.get("type") != "service":
                    print(f"Skipping non-service row: {row}")
                    continue
                
                # Build service data structure
                service_data = {
                    "service": {
                        "name": row["name"],
                        "type": "service",
                        "description": row["description"],
                        "escalation_policy": {
                            "id": DEFAULT_ESCALATION_POLICY_ID,
                            "type": "escalation_policy_reference"
                        },
                        "auto_resolve_timeout": int(row["auto_resolve_timeout"])
                    }
                }
                
                # Call the API to create the service
                create_service(service_data)
    except FileNotFoundError:
        print(f"Error: File '{csv_file_path}' not found.")
    except KeyError as e:
        print(f"Error: Missing required column in CSV - {str(e)}.")
    except Exception as e:
        print(f"Error reading CSV file or creating services: {str(e)}")


if __name__ == "__main__":
    # csv_file_path is the name of the file as long as they share a directory with the script
    # otherwise specify the direct path to the file
    csv_file_path = "services (1) (1) (2) (1).csv"
    read_csv_and_create_services(csv_file_path)
