"""Tests for mock data integrity — ensures dry-run mode works correctly."""

from agents.mock_data import AI_MOCK
from agents.analyst import TechAnalysisResult, KeyPlayer, UseCase


class TestMockDataIntegrity:
    """Verify AI_MOCK is a valid, complete TechAnalysisResult."""

    def test_mock_is_tech_analysis_result(self):
        assert isinstance(AI_MOCK, TechAnalysisResult)

    def test_executive_summary_not_empty(self):
        assert len(AI_MOCK.executive_summary) > 50

    def test_technology_overview_not_empty(self):
        assert len(AI_MOCK.technology_overview) > 50

    def test_maturity_assessment_not_empty(self):
        assert len(AI_MOCK.maturity_assessment) > 50

    def test_market_landscape_not_empty(self):
        assert len(AI_MOCK.market_landscape) > 50

    def test_key_players_exist(self):
        assert len(AI_MOCK.key_players) >= 4
        for player in AI_MOCK.key_players:
            assert isinstance(player, KeyPlayer)
            assert len(player.name) > 0

    def test_use_cases_exist(self):
        assert len(AI_MOCK.use_cases) >= 4
        for uc in AI_MOCK.use_cases:
            assert isinstance(uc, UseCase)
            assert uc.impact_level in ("High", "Medium", "Low")

    def test_strengths_exist(self):
        assert len(AI_MOCK.strengths) >= 4

    def test_limitations_exist(self):
        assert len(AI_MOCK.limitations) >= 4

    def test_adoption_drivers_exist(self):
        assert len(AI_MOCK.adoption_drivers) >= 4

    def test_adoption_barriers_exist(self):
        assert len(AI_MOCK.adoption_barriers) >= 4

    def test_key_trends_exist(self):
        assert len(AI_MOCK.key_trends) >= 5

    def test_risk_factors_exist(self):
        assert len(AI_MOCK.risk_factors) >= 3

    def test_future_outlook_not_empty(self):
        assert len(AI_MOCK.future_outlook) > 30

    def test_mock_serializes_to_json(self):
        json_str = AI_MOCK.model_dump_json()
        restored = TechAnalysisResult.model_validate_json(json_str)
        assert restored.executive_summary == AI_MOCK.executive_summary
