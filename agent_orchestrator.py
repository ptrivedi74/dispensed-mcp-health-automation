import asyncio
import os
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage

load_dotenv()

async def process_patient_triage_automation(patient_id: str):
    """
    Automates the patient intake and clinical summary pipeline using Gemini 3.6 & MCP.
    """
    print(f"\n========================================================")
    print(f"  DISPENSED AUTOMATION ENGINE: Processing {patient_id}")
    print(f"========================================================\n")

    # Define MCP server connection parameters
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_health_server.py"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Automatically discover tools exposed by the MCP server
            tools = await load_mcp_tools(session)

            # Initialize Gemini Model
            llm = ChatGoogleGenerativeAI(
                model="gemini-3.6-flash",
                temperature=0.0,
                google_api_key=os.getenv("GEMINI_API_KEY")
            )

            system_prompt = SystemMessage(
                content="""You are an AI Clinical Operations Automation Agent for Dispensed Telehealth (Australia).

Your Job:
1. Fetch the patient's intake record using the provided MCP tool.
2. Cross-reference their condition with Australian TGA guidelines using `evaluate_tga_eligibility`.
3. Synthesize a concise 3-bullet point "Doctor Pre-Consult Brief" summarizing:
   - Primary complaint & duration
   - Conventional treatments tried & current meds
   - TGA eligibility status & risk flags
4. Save the brief into the EMR using `save_doctor_preconsult_brief`.

Compliance Note: Adhere strictly to factual patient data. Do not invent medical history."""
            )

            # Build ReAct Agent using LangGraph & MCP tools
            agent = create_react_agent(llm, tools, state_modifier=system_prompt)

            user_query = f"Process automation pipeline for Patient ID: {patient_id}"
            
            result = await agent.ainvoke({"messages": [("user", user_query)]})

            # Print Final Execution Result
            print("\n[AUTOMATION SUMMARY OUTPUT]:")
            print(result["messages"][-1].content)

if __name__ == "__main__":
    # Test Case 1: Eligible Chronic Pain Patient
    asyncio.run(process_patient_triage_automation("PAT-9901"))
    
    # Test Case 2: Ineligible Patient (Duration < 6 months, no conventional trial)
    # asyncio.run(process_patient_triage_automation("PAT-9902"))
