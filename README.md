# Friction-Aware Customer Support Assistant (MVP)

## Overview

This project is an MVP (Minimum Viable Product) for a customer support assistant designed to reduce conversational friction, detect user frustration signals, and manage empathetic transitions to human support team members.

Instead of relying heavily on expensive and unpredictable AI throughout the entire conversation, the system utilizes a **hybrid architecture** combining lightweight, rule-based heuristics for live chatting with selective AI usage solely for generating conversation summaries during a human handoff.

The system is designed with a focus on:

* **Human-centered support workflows** that protect user dignity.
* **Cost-and-time-efficient AI orchestration** (Data Minimization).
* **Privacy-conscious design** with explicit user consent.
* **User autonomy** in escalation decisions.
* **Dual-fidelity handoffs** to eliminate the AI "black box" for human agents.

---

## Core Idea

Traditional support systems often rely on either fully automated AI chatbots or immediate escalation to human agents. This project explores a hybrid middle-ground:

1. **Lightweight behavioral signals** track friction locally during the conversation.
2. **Optional, user-controlled escalation** gives the user final say.
3. **AI-assisted summarization** triggers *only* during handoff to respect privacy and slash API costs.

The goal is not to replace human support, but to optimize how users transition between automated assistance and human agents without making them feel digitally illiterate.

---

## Features & System Design

### 1. Rule-Based Frustration Signal Detection

To maximize cost efficiency and data privacy, the system avoids using an LLM for real-time sentiment analysis. Instead, it tracks lightweight conversational heuristics:

* Repeated or closely reworded user questions.
* Aggressive text formatting (ALL CAPS, repeated punctuation like `!!!`).
* Unusually long pauses or disengagement after unresolved system responses.

These signals are treated as interaction patterns, not emotional ground truth, and are used to optionally offer an escalation path.

### 2. User-Controlled Escalation & Privacy Gateways

* **Granular Customer Choice:** Escalation is treated as a user choice, not a system enforcement. Users can accept or decline escalation suggestions. If declined, the state machine gracefully degrades back to standard bot automation while keeping the entry point available.
* **Explicit Customer Consent:** User conversations remain securely inside the application backend database. They are never processed by or transmitted to third-party AI systems until the user explicitly clicks "Yes" to escalate, ensuring complete transparency.
* **Abuse & Prompt-Injection Prevention:** The AI pipeline is protected by stateful input validation. The summarization engine cannot be invoked directly, spammed, or triggered by empty sessions; it requires an active, validated conversation history matrix before execution.

### 3. Dual-Fidelity Human Handoff

When escalation is requested, an LLM compresses the live chat history into a structured summary. To ensure the human agent can keep the chat moving efficiently while maintaining full data integrity, the system utilizes a **Dual-Fidelity Dashboard**:

* **AI Context Summary:** Allows the agent to understand the core issue in 5 seconds so the user *never has to repeat their question*.
* **Raw Chat Log Access:** To solve the AI "black box" problem, human agents retain instant access to unedited raw logs to ensure no critical details or subtle contexts were missed or misinterpreterted by the AI summarizer.

---

## 🌟 UX Spotlight: "Blameless" Copywriting for Inclusivity

A core feature of this MVP is its intentional **Inclusive Communication Design**. System prompts are explicitly written to shift 100% of the technical burden onto the machine, protecting user confidence (especially for the elderly or users with low digital literacy) so they never feel "dumb."

| Trigger Context | Standard "Deflecting" Copy (Biased toward system success) | Redesigned "Blameless" Copy (Inclusive / Accessible) | Why It Works |
| --- | --- | --- | --- |
| **Repetition** | *"It looks like this issue might still not be resolving clearly."* | *"I'm sorry my answers haven't been as helpful as they should be. Let me connect you with one of our team members."* | Admits system failure up front so the user doesn't feel like they are asking the wrong questions. |
| **Confusion** | *"It seems like things might be a bit unclear right now."* | *"This looks like a situation that needs a human touch to get exactly right. Let's get someone on our team to walk through this with you step-by-step."* | Replaces "things are unclear" (which implies the user is being confusing) with a positive framing: the problem simply deserves human care. |
| **General Error** | *"It looks like this issue might need a bit more support. Would you like to talk to a human agent?"* | *"This looks like something that needs a bit more care than I can provide by myself. Would you like to talk directly with one of our friendly team members?"* | Swaps cold, clinical terms like "human agent" for warm, local language ("team members"), while positioning the handover as a feature upgrade. |

---

## Tech Stack

* **Python** (Core application logic & conditional state tracking)
* **Streamlit** (Frontend user UI & Agent dashboard view)
* **SQL Database** (Secure, local conversation state & history tracking)
* **LLM API Interactivity** (Event-driven inference restricted strictly to handoff execution)

---

## Architectural & Business Principles Demonstrated

* **Awareness of Silent Frustration:** Traditional metrics like a "low escalation rate" can be deceptive. Users often abandon apps due to fatigue, confusion, or embarrassment. This system flags disengagement patterns rather than treating silence as customer satisfaction.
* **Drastic TCO (Total Cost of Ownership) Reduction:** Continuously running every single chat message through an LLM for sentiment and response generation is incredibly cost-prohibitive. By using local heuristic rules for the chat and restricting the LLM purely to a single token-optimized summary at the end, API costs are reduced by an estimated 80–90%.
* **Human-in-the-Loop Authority:** AI is used strictly as an information compression tool. It is never treated as an emotional or behavioral authority. Human agents remain responsible for final interpretation, validation, and resolution.

---

## Limitations & Future Roadmap

* Rule-based detection may produce false positives/negatives depending on individual typing habits.
* Pause-based signals are approximate and network-dependent, not definitive.
* **Next Steps:** Conduct usability testing with specific elderly user cohorts to gather qualitative feedback on micro-copy and adjust adaptive escalation thresholds.
