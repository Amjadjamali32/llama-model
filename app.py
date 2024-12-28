from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from datetime import datetime
import pytz
import re  # Importing regular expressions module for text parsing

# Load environment variables
load_dotenv()

# Initialize the Flask app
app = Flask(__name__)

# Retrieve API keys from environment variables
HUGGING_FACE_TOKEN = os.getenv("HUGGING_FACE_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Groq API Configuration
GROQ_MODEL_NAME = "llama-3.1-70b-versatile"  

# Route to generate a report from extracted data
@app.route('/generate_report', methods=['POST'])
def generate_report():
    try:
        # Capture the request timestamp
        request_date, request_time = get_current_date_time_pakistan()

        # Extracting input data
        data = request.json
        complainant_name = data.get("complainant_name")
        complainant_email = data.get("complainant_email")
        complainant_nic = data.get("complainant_nic")
        incident_description = data.get("incident_description")
        
        # Construct the prompt based on user input
        prompt = generate_crime_report_prompt(complainant_name, complainant_email, complainant_nic, incident_description)
        
        # Generate the crime report using the AI model
        ai_response = generate_incident_report_with_groq(prompt)
        
        # Extract specific fields from AI response
        extracted_data = extract_fields_from_ai_response(ai_response)
        
        # Combine extracted data with timestamp
        extracted_data["request_date"] = str(request_date)
        extracted_data["request_time"] = request_time
        
        return jsonify(extracted_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Function to generate a crime report template
def generate_crime_report_prompt(complainant_name, complainant_email, complainant_nic, incident_description):
    return f"""
    Generate a detailed crime incident report with the following details:

    Complainant Information:
    - Name: {complainant_name}
    - Email: {complainant_email}
    - NIC: {complainant_nic}

    Incident Description:
    {incident_description}

    Please generate the following fields based on the provided information:
    - Incident Type: Specify the type of incident in one of the following categories:
        [List of incident types here]
    - Detailed Description of the Incident: Provide a detailed description of the event, including what happened.

    Ensure the report contains all necessary details in a clear and professional manner without additional information or unnecessary formatting. Please do not include any personal opinions or subjective statements in the report. The report should be concise and factual, focusing on the relevant information provided. The report should be structured logically and follow a standard format for crime incident reports. please do not add asterisks. extract the location of incident if provided else unknown. please do not add date and time as it will be added by the system.
    """

# Function to generate a crime report using the Groq API
def generate_incident_report_with_groq(prompt):
    llm = ChatGroq(
        temperature=0,
        groq_api_key=GROQ_API_KEY,
        model_name="llama-3.1-70b-versatile"
    )

    response = llm.invoke(prompt)
    if response and hasattr(response, 'content'):
        response_text = response.content.strip()
    else:
        raise ValueError("Invalid response from Groq API")

    return response_text

# Function to extract specific fields from the AI-generated report
def extract_fields_from_ai_response(ai_response):
    extracted_data = {}
    
    # Use regular expressions to extract specific details from the AI response
    extracted_data['name'] = re.search(r"Name: (.+)", ai_response).group(1) if re.search(r"Name: (.+)", ai_response) else "Unknown"
    extracted_data['email'] = re.search(r"Email: (.+)", ai_response).group(1) if re.search(r"Email: (.+)", ai_response) else "Unknown"
    extracted_data['nic'] = re.search(r"NIC: (.+)", ai_response).group(1) if re.search(r"NIC: (.+)", ai_response) else "Unknown"
    extracted_data['location'] = re.search(r"Location of Incident: (.+)", ai_response).group(1) if re.search(r"Location of Incident: (.+)", ai_response) else "Unknown"
    extracted_data['incident_type'] = re.search(r"Incident Type: (.+)", ai_response).group(1) if re.search(r"Incident Type: (.+)", ai_response) else "Unknown"
    extracted_data['incident_description'] = re.search(r"Detailed Description of the Incident:([\s\S]+)", ai_response).group(1).strip() if re.search(r"Detailed Description of the Incident:([\s\S]+)", ai_response) else "No description provided"

    return extracted_data

#  function to give current date and time
def get_current_date_time_pakistan():
    # Define Pakistan's timezone
    pakistan_timezone = pytz.timezone("Asia/Karachi")
    
    # Get the current date and time in Pakistan's timezone
    current_time_in_pakistan = datetime.now(pakistan_timezone)
    
    # Extract the date and time in 12-hour format
    current_date = current_time_in_pakistan.date()
    current_time = current_time_in_pakistan.strftime("%I:%M:%S %p")  # 12-hour format with AM/PM
    
    return current_date, current_time


# Run the Flask App
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860,debug=True)
