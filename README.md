# 🔬 AI Research Assistant

A multi-agent AI system that researches any topic using live web search and delivers structured, polished Markdown reports — fully automated.

Built with **CrewAI**, **Groq LLMs**, **Serper Search API**, and **Streamlit**.

---

## 🧠 How It Works

Three specialised AI agents work in a sequential pipeline:

| Agent | Role |
|---|---|
| 🔍 **Research Specialist** | Searches the web and collects relevant sources |
| 📊 **Data Analyst** | Synthesises and structures the gathered information |
| ✍️ **Content Writer** | Composes a polished, readable final report |

Each agent produces its own output file, giving you full visibility into every stage of the research process.

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ai-research-assistant.git
cd ai-research-assistant
```

### 2. Create a Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Keys

Copy the template and fill in your keys:

```bash
cp env_template.txt .env
```

Then edit `.env`:

```env
GROQ_API_KEY=your-groq-api-key-here
SERPER_API_KEY=your-serper-api-key-here

RESEARCH_AGENT_LLM=groq/llama-3.3-70b-versatile
ANALYST_AGENT_LLM=groq/llama-3.3-70b-versatile
WRITER_AGENT_LLM=groq/llama-3.3-70b-versatile

RESEARCH_AGENT_TEMPERATURE=0.1
ANALYST_AGENT_TEMPERATURE=0.2
WRITER_AGENT_TEMPERATURE=0.3
```

> 🔑 Get your keys here:
> - **Groq**: [console.groq.com](https://console.groq.com)
> - **Serper**: [serper.dev](https://serper.dev)

### 5. Run the App

```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
ai-research-assistant/
│
├── app.py                  # Streamlit UI
├── crew.py                 # CrewAI crew definition
├── main.py                 # CLI entry point
├── requirements.txt        # Python dependencies
├── env_template.txt        # Environment variable template
│
├── agents/
│   ├── research_specialist.py
│   ├── data_analyst.py
│   └── content_writer.py
│
├── tasks/
│   ├── research_task.py
│   ├── analysis_task.py
│   └── writing_task.py
│
└── (generated outputs)
    ├── research_findings.md
    ├── analysis_report.md
    └── final_report.md
```

---

## ☁️ Deploy on Streamlit Community Cloud

1. Push this repo to **GitHub** (make sure `.env` is in `.gitignore`)
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your repo
3. In **Settings → Secrets**, paste your environment variables in TOML format:

```toml
GROQ_API_KEY = "your-groq-api-key"
SERPER_API_KEY = "your-serper-api-key"
RESEARCH_AGENT_LLM = "groq/llama-3.3-70b-versatile"
ANALYST_AGENT_LLM = "groq/llama-3.3-70b-versatile"
WRITER_AGENT_LLM = "groq/llama-3.3-70b-versatile"
RESEARCH_AGENT_TEMPERATURE = "0.1"
ANALYST_AGENT_TEMPERATURE = "0.2"
WRITER_AGENT_TEMPERATURE = "0.3"
```

4. Click **Deploy** — you'll get a public URL instantly.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| [CrewAI](https://crewai.com) | Multi-agent orchestration framework |
| [Groq](https://groq.com) | Ultra-fast LLM inference |
| [Serper](https://serper.dev) | Google Search API for agents |
| [Streamlit](https://streamlit.io) | Web UI |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | Local environment variable loading |

---

## 📄 License

MIT License — feel free to use, modify, and distribute.
