import os
from crewai import Agent
import streamlit as st
from crewai_tools import SerperDevTool

# Helper to support (.env) and Strealit Cloud
def get_secret(key):
    try:
        return st.secrets[key]
    except Exception:
        return os.getenv(key)

# LLM Configurations
model = get_secret("RESEARCH_AGENT_LLM")
temperature = float(get_secret("RESEARCH_AGENT_TEMPERATURE"))

research_specialist_agent = Agent(
    role="Research Specialist",
    goal="Gather comprehensive and accurate information on given topics from multiple sources",
    backstory = (
                "You are an expert research specialist with years of experience in information gathering "
                "and fact-checking. You have a keen eye for reliable sources and can quickly identify the "
                "most relevant and up-to-date information on any topic."
            ),
    llm=model,
    tools=[SerperDevTool()],
    verbose=True,
)