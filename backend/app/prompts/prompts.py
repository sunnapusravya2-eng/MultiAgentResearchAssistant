from __future__ import annotations

from typing import Any

CHAT_PROMPT_TEMPLATE = """
You are a research assistant. Use the document context and conversation history to answer the user's question.
Context:
{context}

Conversation history:
{history}

Question:
{question}

Provide a concise answer and include citations in the format [Source: filename].
"""

REPORT_PROMPT_TEMPLATE = """
Create a professional research report for the following request.

Title:
{title}

Research question:
{question}

Context:
{context}

Produce a report that includes:
- Executive summary
- Key findings
- Tables or structured bullets if applicable
- Conclusion
- References
"""

def build_chat_prompt(question: str, context: str, history: list[dict[str, str]]) -> str:
    formatted_history = "\n".join(
        f"{entry['role'].capitalize()}: {entry['content']}"
        for entry in history
    )
    return CHAT_PROMPT_TEMPLATE.format(
        question=question,
        context=context or "No relevant document context available.",
        history=formatted_history or "No history available.",
    )

def build_report_prompt(title: str, question: str, context: str) -> str:
    return REPORT_PROMPT_TEMPLATE.format(
        title=title,
        question=question,
        context=context or "No relevant document context available.",
    )