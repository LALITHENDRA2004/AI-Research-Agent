import os
from crewai import Agent
import streamlit as st
from crewai_tools import FileWriterTool

def get_secret(key):
    try:
        return st.secrets[key]
    except Exception:
        return os.getenv(key)

# LLM configurations - Agent specific config
model = get_secret("WRITER_AGENT_LLM")
temperature = float(get_secret("WRITER_AGENT_TEMPERATURE"))

content_writer_agent = Agent(
    role="Expert Content Writer",
    goal=(
        "Create engaging, easy-to-read, and well-structured content that is clear, "
        "informative, and interesting for readers. The content should use simple language, "
        "include examples, bullet points, and proper formatting like headings and subheadings."
    ),
    backstory=(
        "You are a highly skilled content writer who specializes in simplifying complex topics. "
        "You write in a conversational and engaging style similar to ChatGPT responses. "
        "You use clear headings, bullet points, short paragraphs, and real-world examples "
        "to make content easy to understand and enjoyable to read."
    ),
    llm=model,
    tools=[FileWriterTool()],
    verbose=True,
)