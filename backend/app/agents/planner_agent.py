from __future__ import annotations

from langgraph import Graph

from app.agents.citation_agent import CitationAgent
from app.agents.report_agent import ReportAgent
from app.agents.research_agent import ResearchAgent
from app.agents.retriever_agent import RetrieverAgent
from app.agents.summarizer_agent import SummarizerAgent


class PlannerAgent:
    def __init__(self) -> None:
        self.graph = Graph()
        self.retriever_agent = RetrieverAgent()
        self.research_agent = ResearchAgent()
        self.summarizer_agent = SummarizerAgent()
        self.citation_agent = CitationAgent()
        self.report_agent = ReportAgent()

    def plan(self, question: str, conversation_id: str) -> dict[str, str]:
        retrieved = self.retriever_agent.retrieve(question)
        research_output = self.research_agent.research(question, retrieved)
        summary = self.summarizer_agent.summarize(research_output)
        citations = self.citation_agent.verify(summary, retrieved)
        report = self.report_agent.build_report(question, summary, citations)

        return {
            "answer": research_output,
            "summary": summary,
            "citations": citations,
            "report_text": report,
        }