# Friction-Aware Customer Support Assistant (MVP)

## Overview

This project is an MVP (Minimum Viable Product) for a customer support assistant designed to reduce conversational friction, detect possible user frustration signals, and support smoother escalation to human agents.

Instead of relying heavily on AI throughout the entire conversation, the system uses a hybrid architecture combining rule-based heuristics and selective AI usage. AI is only invoked when the user explicitly requests human escalation, where it is used to generate a conversation summary for support agents.

The system is designed with a focus on:

* Human-centered support workflows
* Cost-efficient AI usage
* Privacy-conscious design
* User autonomy in escalation decisions
* Reducing friction in customer support interactions

---

## Core Idea

Traditional support systems often rely on either:

* fully automated chatbots, or
* immediate escalation to human agents

This project explores a hybrid middle-ground:

* lightweight behavioral signals during conversation
* optional, user-controlled escalation
* AI-assisted summarization only during handoff

The goal is not to replace human support, but to improve how users transition between automated assistance and human agents.

---

## Features

### 1. Rule-Based Frustration Signal Detection

The system does **not** use an LLM for real-time frustration detection.

Instead, it uses lightweight heuristics such as:

* repeated or reworded questions
* aggressive formatting (`ALL CAPS`, repeated punctuation like `!!!`)
* unusually long pauses after unresolved responses

These signals are treated as *interaction patterns*, not emotional ground truth, and are used to optionally suggest escalation.

---

### 2. User-Controlled Escalation Flow

When potential frustration signals are detected:

* the system suggests human escalation
* the user may accept or decline
* if declined, the conversation continues normally

Escalation is always optional and user-driven.

---

### 3. AI-Assisted Human Handoff

When escalation is requested:

1. full conversation history is preserved
2. an AI-generated summary is created
3. both summary and full chat are passed to the human support agent

The summary is intended to:

* reduce repeated questioning
* speed up agent understanding
* improve continuity of conversation

---

## Design Principles

This system is built around a set of human-centered and system-aware design principles.

---

### 1. Human-in-the-Loop Decision Making

Human support agents remain the final authority in interpreting user intent and resolving issues.

* AI-generated summaries are assistive, not authoritative
* full conversation logs are always available
* agents may verify or override AI interpretations

This ensures that AI supports decision-making without replacing human judgment in ambiguous contexts.

---

### 2. Hybrid Intelligence: Separation of Responsibilities

The system separates concerns between rule-based logic and AI:

* rule-based heuristics handle real-time interaction signals
* AI is used only for structured language tasks (summarization during escalation)

This separation improves:

* interpretability
* reliability
* cost efficiency

---

### 3. Cost-Aware AI Usage

AI is not continuously invoked during conversations.

Instead:

* real-time detection uses lightweight logic
* AI is only triggered during escalation events

This reduces:

* API costs
* latency
* unnecessary data processing

while preserving AI value where it is most useful.

---

### 4. Privacy-Conscious Design

User conversations are not continuously processed by external AI systems.

* live chats remain within the application backend
* AI is used only after explicit escalation
* AI usage is intentional rather than passive

This ensures transparency in when and why external AI processing occurs.

---

### 5. Human-Centered Escalation Design

Escalation is treated as a user choice, not a system enforcement.

* users can accept or decline escalation suggestions
* escalation prompts are phrased in a non-blaming tone
* the system avoids implying user error or incompetence

The goal is to reduce emotional friction during support interactions.

---

### 6. Awareness of Silent Frustration

Traditional metrics such as “low escalation rate” do not always indicate success.

Users may stop engaging due to:

* confusion
* fatigue
* embarrassment
* unresolved frustration

The system considers interaction patterns (e.g., repetition, pauses) as potential signals of disengagement rather than treating silence as satisfaction.

---

### 7. Inclusive Communication Design

The system is designed to accommodate different user interaction styles, including:

* low digital literacy users
* elderly users
* users experiencing cognitive overload

System messages are intentionally written in a supportive, non-blaming tone, focusing on system limitations rather than user failure.

---

### 8. AI as a Support Tool, Not an Emotional Authority

AI is used only for summarization and information compression during escalation.

It is not used as the sole source of:

* emotional interpretation
* frustration detection
* behavioral judgment

This is due to known limitations in contextual, cultural, and behavioral interpretation. Human agents remain responsible for final interpretation and resolution.

---

## Tech Stack

* Python
* Streamlit
* SQL database

Core implementation uses:

* rule-based conditional logic
* conversation state tracking
* event-driven escalation workflow
* AI-based summarization during escalation

---

## Limitations

* rule-based detection may produce false positives/negatives
* pause-based signals are approximate, not definitive
* AI summarization may omit subtle context
* no advanced sentiment model is currently used

---

## Future Improvements

* LLM-based sentiment and intent analysis (optional hybrid layer)
* adaptive escalation thresholds
* usability testing and feedback collection
* analytics on escalation outcomes
* improved personalization of support messaging
* multilingual support

---

## Project Status

MVP / Prototype stage:

* functional rule-based detection system
* user-controlled escalation flow
* AI-assisted summarization for human handoff
* SQL-backed conversation storage

This project is exploratory and focuses on human-centered AI system design, conversational workflows, and support interaction optimization.
