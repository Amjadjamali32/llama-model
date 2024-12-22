import re
from pprint import pprint

# Simulated response from the API
incident_report = """
**Incident Report Number:** 2024-12-21-001

**Date and Time of Incident:** 2024-12-21 14:30

**Location:** 123 Main St, Cityville

**Incident Type:** Theft

**Complainant Information:**

* **Name:** John Doe
* **Contact Information:**
    + Phone Number: 555-1234
    + Email: john.doe@example.com

**Incident Overview:**
On 2024-12-21 at approximately 14:30, John Doe reported an incident involving Theft at 123 Main St, Cityville.

**Incident Details:**
The complainant reported a theft where their wallet was stolen from their bag while shopping. The wallet contained personal identification, credit cards, and cash. The complainant stated that they were unaware of the theft until they reached for their wallet and discovered it was missing.

**Actions Taken:**

* **Police Response:** The police were notified, and an investigation is currently underway. Officers are reviewing security footage and interviewing potential witnesses to gather more information about the incident.
* **Witnesses:** At this time, there are no witnesses who have come forward with information about the incident. However, the investigation is ongoing, and we are encouraging anyone with information to contact the authorities.

**Signature of Complainant:**
John Doe
**Date:** 2024-12-21

**Officer's Notes:** This report will be updated as more information becomes available. The complainant has been provided with a copy of this report and has been informed of the next steps in the investigation.

**Distribution:**

* Original: Police Department File
* Copy: Complainant (John Doe)

Please note that this report is a formal document and any amendments or updates will be made in accordance with police procedures.
"""

# Regular expressions to extract various parts of the report
incident_report_number = re.search(r"\*\*Incident Report Number:\*\* ([\S\s]+?)\n", incident_report).group(1)
incident_datetime = re.search(r"\*\*Date and Time of Incident:\*\* ([\S\s]+?)\n", incident_report).group(1)
location = re.search(r"\*\*Location:\*\* ([\S\s]+?)\n", incident_report).group(1)
incident_type = re.search(r"\*\*Incident Type:\*\* ([\S\s]+?)\n", incident_report).group(1)
complainant_name = re.search(r"\*\*Name:\*\* ([\S\s]+?)\n", incident_report).group(1)
complainant_phone = re.search(r"\+ Phone Number: ([\S\s]+?)\n", incident_report).group(1)
complainant_email = re.search(r"\+ Email: ([\S\s]+?)\n", incident_report).group(1)
incident_description = re.search(r"\*\*Incident Details:\*\*([\S\s]+?)\*\*Actions Taken:", incident_report).group(1).strip()
police_response = re.search(r"\*\*Police Response:\*\* ([\S\s]+?)\n", incident_report).group(1)
witnesses = re.search(r"\*\*Witnesses:\*\* ([\S\s]+?)\n", incident_report).group(1)
officer_notes = re.search(r"\*\*Officer's Notes:\*\* ([\S\s]+?)\n", incident_report).group(1)
distribution = re.search(r"\*\*Distribution:\*\*([\S\s]+?)\n", incident_report).group(1).strip()

# Additional data to include
complainant_signature_image = "http://example.com/signature_image.jpg"  # URL or file path for the image
police_station_name = "Cityville Police Department"
report_unique_number = "RPN-2024-12-21-001"

# Create a dictionary with the extracted values and additional data
extracted_data = {
    "incident_report_number": incident_report_number,
    "incident_datetime": incident_datetime,
    "location": location,
    "incident_type": incident_type,
    "complainant_name": complainant_name,
    "complainant_phone": complainant_phone,
    "complainant_email": complainant_email,
    "incident_description": incident_description,
    "police_response": police_response,
    "witnesses": witnesses,
    "officer_notes": officer_notes,
    "distribution": distribution,
    "complainant_signature_image": complainant_signature_image,
    "police_station_name": police_station_name,
    "report_unique_number": report_unique_number
}

# Output the extracted data
pprint(extracted_data)
