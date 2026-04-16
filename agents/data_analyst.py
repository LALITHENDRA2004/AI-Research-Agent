import os
from crewai import Agent
import streamlit as st
from crewai_tools import FileReadTool

def get_secret(key):
    try:
        return st.secrets[key]
    except Exception:
        return os.getenv(key)

# LLM configurations - Agent specific config
model = get_secret("ANALYST_AGENT_LLM")
temperature = float(get_secret("ANALYST_AGENT_TEMPERATURE"))

data_analyst_agent = Agent(
    role="Data Analyst",
    goal="Analyze gathered information to extract key insights, patterns, and conclusions",
    backstory = (
                "You are a skilled data analyst with expertise in synthesizing complex "
                "information into actionable insights. You excel at identifying patterns, trends, "
                "and key findings from research data."
            ),
    llm=model,
    tools=[FileReadTool()],
    verbose=True,
)