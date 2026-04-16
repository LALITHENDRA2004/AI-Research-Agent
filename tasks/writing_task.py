import textwrap

from crewai import Task
from agents.content_writer import content_writer_agent
from tasks.analysis_task import analysis_task
from tasks.research_task import research_task


writing_task = Task(
    agent=content_writer_agent,
    description=textwrap.dedent("""
        Create a highly engaging and easy-to-read report on the topic: {topic}

        IMPORTANT WRITING STYLE:
        - Use simple and clear language (avoid complex jargon)
        - Write in a conversational tone (like ChatGPT)
        - Break content into small paragraphs
        - Use proper headings and subheadings
        - Include bullet points wherever possible
        - Add real-world examples to explain concepts
        - Make the content interesting and easy to follow

        STRUCTURE:
        1. Executive Summary (short and clear)
        2. Introduction (simple explanation)
        3. Key Concepts (with bullet points)
        4. Detailed Explanation (with examples)
        5. Insights / Trends
        6. Conclusion (clear and practical)

        FORMATTING RULES:
        - Use markdown headings (##, ###)
        - Use bullet points (-)
        - Highlight important points clearly
        - Keep readability as top priority

        The final output should feel like a high-quality ChatGPT explanation, not a formal academic report.
        """),
     expected_output="""
        A well-structured, engaging report written in simple language with headings,
        bullet points, and examples, making it easy and interesting to read.
        """,
    input_variables=["topic"],
    context=[research_task, analysis_task],
    output_file="final_report.md"
    )