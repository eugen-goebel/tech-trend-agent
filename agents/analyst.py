"""
Analysis Agent — Transforms raw research into structured technology insights.

Uses structured outputs (Pydantic) and adaptive thinking to produce
a comprehensive TechAnalysisResult from unstructured research text.
"""

from pydantic import BaseModel
import anthropic

from typing import Literal


# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------

class KeyPlayer(BaseModel):
    """A significant company or organization in the technology space."""
    name: str
    description: str
    focus_area: str
    market_position: str


class UseCase(BaseModel):
    """A real-world application of the technology."""
    title: str
    description: str
    industry: str
    impact_level: Literal["High", "Medium", "Low"]


class TechAnalysisResult(BaseModel):
    """Complete structured analysis of a technology trend."""
    executive_summary: str
    technology_overview: str
    maturity_assessment: str
    market_landscape: str
    key_players: list[KeyPlayer]
    use_cases: list[UseCase]
    strengths: list[str]
    limitations: list[str]
    adoption_drivers: list[str]
    adoption_barriers: list[str]
    future_outlook: str
    key_trends: list[str]
    risk_factors: list[str]


# ---------------------------------------------------------------------------
# Agent
# ---------------------------------------------------------------------------

class AnalysisAgent:
    """
    Analyzes raw technology research and produces a structured
    TechAnalysisResult using the Anthropic structured output API.
    """

    def __init__(self, client: anthropic.Anthropic, model: str = "claude-opus-4-6"):
        self.client = client
        self.model = model

    def analyze(self, technology: str, research_brief: str) -> TechAnalysisResult:
        """
        Parse unstructured research text into a TechAnalysisResult.

        Args:
            technology:     Name of the technology being analyzed
            research_brief: Raw text from the ResearchAgent

        Returns:
            Validated TechAnalysisResult instance
        """
        system_prompt = (
            "You are a senior technology analyst specializing in emerging tech trends. "
            "Given raw research data, produce a comprehensive and structured analysis. "
            "Be specific with data points, market figures, and concrete examples. "
            "Provide at least 5 key players, 5 use cases, 5 strengths, 5 limitations, "
            "5 adoption drivers, 5 adoption barriers, 7 key trends, and 5 risk factors."
        )

        response = self.client.messages.parse(
            model=self.model,
            max_tokens=16000,
            thinking={"type": "adaptive"},
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Analyze the following research about {technology} and produce "
                        f"a complete technology trend report.\n\n"
                        f"RESEARCH DATA:\n{research_brief}"
                    ),
                }
            ],
            output_format=TechAnalysisResult,
        )

        return response.parsed_output
