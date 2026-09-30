import json
import logging
from typing import Dict, Any
from mcp.server.fastmcp import FastMCP

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Dispensed-Health-MCP")

# Initialize FastMCP Server
mcp = FastMCP("Dispensed_Health_Integration_Server")

# Mock Internal Database (Simulating Dispensed Telehealth DB & Health APIs)
MOCK_PATIENT_DB = {
    "PAT-9901": {
        "patient_id": "PAT-9901",
        "age": 34,
        "state": "NSW",
        "primary_symptom": "Chronic Neuropathic Pain",
        "symptom_duration_months": 8,
        "tried_conventional_treatments": True,
        "past_treatments": ["Physiotherapy", "NSAIDs", "Gabapentin"],
        "history_of_psychosis": False,
        "current_medications": ["Sertraline 50mg"],
        "medicare_verified": True
    },
    "PAT-9902": {
        "patient_id": "PAT-9902",
        "age": 22,
        "state": "VIC",
        "primary_symptom": "Insomnia & Mild Anxiety",
        "symptom_duration_months": 2,  # < 6 months requirement
        "tried_conventional_treatments": False,
        "past_treatments": [],
        "history_of_psychosis": False,
        "current_medications": [],
        "medicare_verified": True
    }
}

# --- MCP TOOLS ---

@mcp.tool()
def fetch_patient_intake_record(patient_id: str) -> Dict[str, Any]:
    """
    Fetches raw patient questionnaire and pre-screening intake data.
    Complies with Australian Privacy Act by returning structured clinical indicators.
    """
    logger.info(f"Retrieving intake data for Patient ID: {patient_id}")
    patient = MOCK_PATIENT_DB.get(patient_id.upper())
    if not patient:
        return {"error": f"Patient ID {patient_id} not found."}
    return patient


@mcp.tool()
def evaluate_tga_eligibility(
    symptom_duration_months: int,
    tried_conventional_treatments: bool,
    history_of_psychosis: bool
) -> Dict[str, Any]:
    """
    Evaluates Australian TGA / SAS / Authorised Prescriber clinical eligibility criteria:
    1. Condition must be chronic (>6 months).
    2. First-line / conventional treatments must have been evaluated or tried.
    3. No contraindications (e.g., active psychosis history for THC-based therapies).
    """
    reasons = []
    eligible = True

    if symptom_duration_months < 6:
        eligible = False
        reasons.append("Symptom duration is under 6 months (TGA chronic condition guideline requires >= 6 months).")

    if not tried_conventional_treatments:
        eligible = False
        reasons.append("Patient has not tried conventional first-line treatments prior to alternative therapy.")

    if history_of_psychosis:
        eligible = False
        reasons.append("Contraindication detected: History of psychosis flagged.")

    return {
        "eligible_for_consult": eligible,
        "exclusion_reasons": reasons if not eligible else ["None"],
        "tga_pathway_suggested": "Authorised Prescriber Scheme" if eligible else "N/A"
    }


@mcp.tool()
def save_doctor_preconsult_brief(
    patient_id: str,
    eligibility_status: str,
    summary_notes: str,
    recommended_action: str
) -> Dict[str, Any]:
    """
    Saves the AI-generated clinical summary brief directly into the Dispensed EMR / Doctor Portal.
    """
    logger.info(f"Saving Doctor Brief for {patient_id}...")
    # Simulation of database record update
    brief_record = {
        "patient_id": patient_id,
        "eligibility_status": eligibility_status,
        "summary_notes": summary_notes,
        "recommended_action": recommended_action,
        "status": "READY_FOR_DOCTOR_REVIEW"
    }
    return {
        "success": True,
        "message": f"Pre-consultation brief successfully attached to clinic record for {patient_id}.",
        "record": brief_record
    }

if __name__ == "__main__":
    mcp.run()