import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

# 🔥 FORCE Groq BEFORE importing crew
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_BASE_URL"] = "https://api.groq.com/openai/v1"

# DEBUG (important)
print("API BASE:", os.environ.get("OPENAI_BASE_URL"))

# NOW import crew
from crew import research_crew


def run(topic: str):
    result = research_crew.kickoff(inputs={"topic": topic})

    print("-" * 50)
    print(result)
    print("-" * 50)


if __name__ == "__main__":
    topic = "AI Agents"
    run(topic)