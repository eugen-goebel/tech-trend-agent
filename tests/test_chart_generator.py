"""Tests for chart generation."""

from io import BytesIO

from agents.analyst import TechAnalysisResult, KeyPlayer, UseCase
from agents.mock_data import AI_MOCK
from utils.chart_generator import (
    create_key_players_chart,
    create_use_case_impact_chart,
    _estimate_market_relevance,
)


def _minimal_analysis():
    return TechAnalysisResult(
        executive_summary="Summary.",
        technology_overview="Overview.",
        maturity_assessment="Mature.",
        market_landscape="Growing.",
        key_players=[
            KeyPlayer(name="Acme", description="A company", focus_area="AI", market_position="Market leader"),
            KeyPlayer(name="Beta", description="Another", focus_area="ML", market_position="Emerging player"),
        ],
        use_cases=[
            UseCase(title="Automation", description="Automate tasks", industry="Tech", impact_level="High"),
            UseCase(title="Analytics", description="Analyze data", industry="Finance", impact_level="Medium"),
            UseCase(title="Support", description="Chat support", industry="Retail", impact_level="Low"),
        ],
        strengths=["Fast"],
        limitations=["Expensive"],
        adoption_drivers=["Cost savings"],
        adoption_barriers=["Complexity"],
        future_outlook="Positive.",
        key_trends=["Growth"],
        risk_factors=["Regulation"],
    )


class TestKeyPlayersChart:

    def test_returns_bytesio(self):
        buf = create_key_players_chart(_minimal_analysis())
        assert isinstance(buf, BytesIO)

    def test_png_header(self):
        buf = create_key_players_chart(_minimal_analysis())
        header = buf.read(8)
        assert header[:4] == b"\x89PNG"

    def test_buffer_not_empty(self):
        buf = create_key_players_chart(_minimal_analysis())
        data = buf.read()
        assert len(data) > 1000

    def test_works_with_mock_data(self):
        buf = create_key_players_chart(AI_MOCK)
        assert isinstance(buf, BytesIO)
        assert len(buf.read()) > 1000


class TestUseCaseImpactChart:

    def test_returns_bytesio(self):
        buf = create_use_case_impact_chart(_minimal_analysis())
        assert isinstance(buf, BytesIO)

    def test_png_header(self):
        buf = create_use_case_impact_chart(_minimal_analysis())
        header = buf.read(8)
        assert header[:4] == b"\x89PNG"

    def test_works_with_mock_data(self):
        buf = create_use_case_impact_chart(AI_MOCK)
        assert isinstance(buf, BytesIO)
        assert len(buf.read()) > 1000


class TestMarketRelevanceScoring:

    def test_market_leader_scores_5(self):
        assert _estimate_market_relevance("Global market leader") == 5

    def test_emerging_scores_1(self):
        assert _estimate_market_relevance("Emerging player") == 1

    def test_strong_scores_3(self):
        assert _estimate_market_relevance("Strong competitor") == 3

    def test_unknown_defaults_to_3(self):
        assert _estimate_market_relevance("Some random position") == 3
