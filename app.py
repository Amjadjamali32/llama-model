from flask import Flask, request, jsonify
import requests
import re
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq

# Initialize the Flask app
app = Flask(__name__)

# Hugging Face API Configuration
HUGGING_FACE_TOKEN = "Bearer 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"  # Replace with your Hugging Face token
MODEL_URL = "https://api-inference.huggingface.co/models/criminal-case-classifier2"

headers = {
    "Authorization": f"Bearer {HUGGING_FACE_TOKEN}",
    "Content-Type": "application/json"
}

# Groq API Configuration
GROQ_API_KEY = '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'  # Replace with your Groq API key

# Route to extract data from the input crime report template
@app.route('/extract_report_data', methods=['POST'])
def extract_report_data():
    try:
        # Simulated or user-provided incident report
        incident_report = request.json.get("incident_report", "")

        # Regular expressions to extract fields
        data = {
            "incident_report_number": re.search(r"\*\*Incident Report Number:\*\* ([\S\s]+?)\n", incident_report).group(1),
            "incident_datetime": re.search(r"\*\*Date and Time of Incident:\*\* ([\S\s]+?)\n", incident_report).group(1),
            "location": re.search(r"\*\*Location:\*\* ([\S\s]+?)\n", incident_report).group(1),
            "incident_type": re.search(r"\*\*Incident Type:\*\* ([\S\s]+?)\n", incident_report).group(1),
            "complainant_name": re.search(r"\*\*Name:\*\* ([\S\s]+?)\n", incident_report).group(1),
            "complainant_phone": re.search(r"\+ Phone Number: ([\S\s]+?)\n", incident_report).group(1),
            "complainant_email": re.search(r"\+ Email: ([\S\s]+?)\n", incident_report).group(1),
            "incident_description": re.search(r"\*\*Incident Details:\*\*([\S\s]+?)\*\*Actions Taken:", incident_report).group(1).strip(),
            "police_response": re.search(r"\*\*Police Response:\*\* ([\S\s]+?)\n", incident_report).group(1),
            "witnesses": re.search(r"\*\*Witnesses:\*\* ([\S\s]+?)\n", incident_report).group(1),
            "officer_notes": re.search(r"\*\*Officer's Notes:\*\* ([\S\s]+?)\n", incident_report).group(1),
            "distribution": re.search(r"\*\*Distribution:\*\*([\S\s]+?)\n", incident_report).group(1).strip(),
        }

        return jsonify({"extracted_data": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Route to generate a report from extracted data
@app.route('/generate_report', methods=['POST'])
def generate_report():
    try:
        # Extracting input data
        data = request.json
        prompt = generate_crime_report(
            data["incident_datetime"].split()[0],
            data["incident_datetime"].split()[1],
            data["location"],
            data["incident_type"],
            data["complainant_name"],
            data["complainant_phone"],
            data["complainant_email"],
            data["incident_description"],
            data["police_response"]
        )

        # Generate report using Groq API
        report = generate_incident_report_with_groq(prompt)

        return jsonify({"incident_report": report})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Function to generate a report template
def generate_crime_report(incident_date, incident_time, location, incident_type, complainant_name, complainant_phone, complainant_email, incident_description, police_response):
    return f"""
    Generate a formal crime incident report with the following details:

    Report Number: [Auto-generate report number]

    Date and Time of Incident: {incident_date} {incident_time}
    Location: {location}
    Incident Type: {incident_type}
    Complainant Name: {complainant_name}
    Complainant Contact Information:
    - Phone Number: {complainant_phone}
    - Email: {complainant_email}

    Incident Overview:  
    On {incident_date} at approximately {incident_time}, {complainant_name} reported an incident involving {incident_type} at {location}.

    Incident Details:  
    {incident_description}

    Actions Taken:  
    - Police Response: {police_response}
    - Witnesses: [Insert any witness statements or details, if applicable]

    Signature of Complainant:  
    {complainant_name}
    Date: [Insert Date of Report Submission]

    Please ensure the report is clear, formal, and professional.
    """

# Function to call Groq API for report generation
def generate_incident_report_with_groq(prompt):
    llm = ChatGroq(
        temperature=0,
        groq_api_key=GROQ_API_KEY,
        model_name="llama-3.1-70b-versatile"
    )
    response = llm.invoke(prompt)
    return response.content.strip()

# Run the Flask App
if __name__ == "__main__":
    app.run(debug=True)
