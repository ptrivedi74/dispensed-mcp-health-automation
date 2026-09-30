# Dispensed Health — MCP Patient Triage & Clinical Automation Engine

An autonomous, Model Context Protocol (MCP) driven AI agent built to eliminate manual clinical operations for telehealth platforms operating across Australia (TGA / AHPRA guidelines), NZ, and the UK.

---

## Problem Statement & Operational Impact

Telehealth platforms spend significant manual hours on pre-consultation admin:
1. Reviewing multi-page patient intake questionnaires.
2. Checking eligibility against regulatory rules (e.g., TGA requirements for chronic condition duration ≥ 6 months and first-line treatment history).
3. Flagging psychiatric or substance contraindications.
4. Synthesizing medical histories into pre-consultation briefs for prescribers.

### **The Solution**
This tool uses an **MCP Server/Client Architecture** to securely bridge LLMs (Gemini 2.5 Flash) with internal Electronic Medical Record (EMR) databases and regulatory compliance rules.

* **Speed:** Reduces pre-consult summary generation from ~5–7 minutes to **< 3 seconds**.
* **Safety:** Programmatic guardrails reject non-compliant candidates before doctor review, reducing clinical overhead.
* **Privacy:** Pre-screens data locally before sending anonymized payloads to the LLM agent.

---

## System Architecture

text
+-----------------------+        MCP Protocol        +----------------------------+
|  Agent Orchestrator   |  <---------------------->  |     MCP Health Server      |
|  (LangChain/Gemini)   |    Tools & Structured Data |  (mcp_health_server.py)    |
+-----------------------+                            +----------------------------+
            |                                                      |
            v                                                      v
  Generates Clinical Brief                               Checks TGA / EMR Data
