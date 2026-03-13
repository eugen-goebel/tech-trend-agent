"""Tests for Pydantic data models (TechAnalysisResult, KeyPlayer, UseCase)."""

import pytest
from pydantic import ValidationError
from agents.analyst import TechAnalysisResult, KeyPlayer, UseCase


class TestKeyPlayer:
    """Validate KeyPlayer model."""

    def test_valid_player(self):
        player = KeyPlayer(
            name="OpenAI",
            description="AI research company.",
            focus_area="Foundation models",
            market_position="Market leader",
        )
        assert player.name == "OpenAI"

    def test_missing_field_raises(self):
        with pytest.raises(ValidationError):
            KeyPlayer(name="OpenAI", description="Test")

    def test_json_roundtrip(self):
        player = KeyPlayer(
            name="Test", description="Desc",
            focus_area="AI", market_position="Leader",
        )
        json_str = player.model_dump_json()
        restored = KeyPlayer.model_validate_json(json_str)
        assert restored.name == player.name


class TestUseCase:
    """Validate UseCase model."""

    def test_valid_use_case(self):
        uc = UseCase(
            title="Code Generation",
            description="AI writes code.",
            industry="Software",
            impact_level="High",
        )
        assert uc.impact_level == "High"

    def test_invalid_impact_level(self):
        with pytest.raises(ValidationError):
            UseCase(
                title="Test", description="Desc",
                industry="Tech", impact_level="Extreme",
            )

    def test_valid_impact_levels(self):
        for level in ["High", "Medium", "Low"]:
            uc = UseCase(
                title="T", description="D",
                industry="I", impact_level=level,
            )
            assert uc.impact_level == level


class TestTechAnalysisResult:
    """Validate the full TechAnalysisResult model."""

    @pytest.fixture
    def valid_analysis(self):
        return TechAnalysisResult(
            executive_summary="Summary.",
            technology_overview="Overview.",
            maturity_assessment="Mature.",
            market_landscape="Growing.",
            key_players=[
                KeyPlayer(name="X", description="D", focus_area="F", market_position="P")
            ],
            use_cases=[
                UseCase(title="T", description="D", industry="I", impact_level="High")
            ],
            strengths=["Strong"],
            limitations=["Limited"],
            adoption_drivers=["Cost"],
            adoption_barriers=["Talent"],
            future_outlook="Bright.",
            key_trends=["AI agents"],
            risk_factors=["Regulation"],
        )

    def test_valid_creation(self, valid_analysis):
        assert valid_analysis.executive_summary == "Summary."
        assert len(valid_analysis.key_players) == 1

    def test_missing_required_field(self):
        with pytest.raises(ValidationError):
            TechAnalysisResult(
                executive_summary="Test",
                technology_overview="Test",
            )

    def test_nested_access(self, valid_analysis):
        assert valid_analysis.key_players[0].name == "X"
        assert valid_analysis.use_cases[0].impact_level == "High"

    def test_serialization(self, valid_analysis):
        data = valid_analysis.model_dump()
        assert "key_players" in data
        assert "use_cases" in data

    def test_json_roundtrip(self, valid_analysis):
        json_str = valid_analysis.model_dump_json()
        restored = TechAnalysisResult.model_validate_json(json_str)
        assert restored.executive_summary == valid_analysis.executive_summary
        assert len(restored.key_players) == len(valid_analysis.key_players)
