# Adaptive Support System

A lightweight customer support prototype that detects signs of user friction, adapts escalation behavior, and generates AI summaries for human support handoff.

## Features

- Chat-based customer support interface
- Lightweight frustration detection using behavioral signals such as repetition, capitalization, punctuation, and inactivity
- Human support suggestions when frustration reaches a threshold
- Users can decline escalation and continue chatting without being repeatedly prompted
- Human support remains available after escalation has been offered
- AI-generated conversation summaries for support handoff
- SQLite storage for messages and escalated cases
- Agent dashboard showing the frustration score, AI summary, and full conversation
- Small simulated typing indicator for a more natural chat experience

## Tech Stack

- Python
- Streamlit
- SQLite
- Hugging Face Transformers
- FLAN-T5
- PyTorch

## How It Works

The system monitors the conversation for simple behavioral signals that may indicate friction. When the frustration score reaches a threshold, the user is given the option to connect with human support.

If the user declines, they can continue chatting without receiving repeated escalation prompts. Human support remains available if they decide to request it later.

When a conversation is escalated, the system generates a short AI summary and stores the case in SQLite. The agent dashboard displays the summary, frustration score, and original conversation for reference.

## Running the Project

Install the dependencies:

```bash
pip install -r requirements.txt
```

Run the customer support interface:

```bash
streamlit run esapp.py
```

Run the agent dashboard:

```bash
PYTHONPATH=. streamlit run dashbord/agent_ui.py
```

## Project Structure

```text
adaptive-support-system/
├── ai/             # AI summarization
├── core/           # Chatbot, frustration detection, and escalation logic
├── dashbord/       # Human support agent interface
├── data/           # SQLite database logic
├── esapp.py        # Customer-facing Streamlit app
└── requirements.txt
```

## Current Status

This project is a working prototype with opportunities for further improvement, including more robust friction detection, improved AI summarization, and additional UI polish.
