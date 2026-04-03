"""Tests for technology comparison mode."""

import os
import subprocess
import sys

import pytest
from unittest.mock import MagicMock, patch

from agents.analyst import TechAnalysisResult, KeyPlayer, UseCase
from agents.mock_data import AI_MOCK, BLOCKCHAIN_MOCK, COMPARISON_MOCKS
from utils.comparison_report import generate_comparison_report


@pytest.fixture
def minimal_analysis():
    """Minimal TechAnalysisResult for testing."""
    return TechAnalysisResult(
        executive_summary="Summary text.",
        technology_overview="Overview text.",
        maturity_assessment="Maturity text.",
        market_landscape="Market text.",
        key_players=[
            KeyPlayer(name="Company A", description="Desc",
                      focus_area="Focus", market_position="Leading"),
        ],
        use_cases=[
            UseCase(title="Use 1", description="Desc",
                    industry="Tech", impact_level="High"),
        ],
        strengths=["Strength 1"],
        limitations=["Limitation 1"],
        adoption_drivers=["Driver 1"],
        adoption_barriers=["Barrier 1"],
        future_outlook="Outlook text.",
        key_trends=["Trend 1"],
        risk_factors=["Risk 1"],
    )


class TestComparisonMocks:
    def test_comparison_mocks_has_ai(self):
        assert "Artificial Intelligence" in COMPARISON_MOCKS

    def test_comparison_mocks_has_blockchain(self):
        assert "Blockchain" in COMPARISON_MOCKS

    def test_blockchain_mock_is_valid(self):
        assert isinstance(BLOCKCHAIN_MOCK, TechAnalysisResult)
        assert len(BLOCKCHAIN_MOCK.key_players) >= 5
        assert len(BLOCKCHAIN_MOCK.use_cases) >= 5
        assert len(BLOCKCHAIN_MOCK.key_trends) >= 5

    def test_blockchain_mock_content(self):
        assert "Blockchain" in BLOCKCHAIN_MOCK.technology_overview
        assert len(BLOCKCHAIN_MOCK.executive_summary) > 100


class TestComparisonReport:
    def test_generates_docx_file(self, tmp_path, minimal_analysis):
        path = generate_comparison_report(
            ["Tech A", "Tech B"],
            [minimal_analysis, minimal_analysis],
            output_dir=str(tmp_path),
        )
        assert os.path.isfile(path)
        assert path.endswith(".docx")

    def test_filename_contains_technologies(self, tmp_path, minimal_analysis):
        path = generate_comparison_report(
            ["Alpha", "Beta"],
            [minimal_analysis, minimal_analysis],
            output_dir=str(tmp_path),
        )
        basename = os.path.basename(path)
        assert "alpha" in basename
        assert "beta" in basename
        assert "_vs_" in basename

    def test_three_technologies(self, tmp_path, minimal_analysis):
        path = generate_comparison_report(
            ["A", "B", "C"],
            [minimal_analysis, minimal_analysis, minimal_analysis],
            output_dir=str(tmp_path),
        )
        assert os.path.isfile(path)

    def test_with_real_mock_data(self, tmp_path):
        path = generate_comparison_report(
            ["Artificial Intelligence", "Blockchain"],
            [AI_MOCK, BLOCKCHAIN_MOCK],
            output_dir=str(tmp_path),
        )
        assert os.path.isfile(path)
        assert os.path.getsize(path) > 10000

    def test_creates_output_directory(self, tmp_path, minimal_analysis):
        out = str(tmp_path / "nested" / "dir")
        path = generate_comparison_report(
            ["X", "Y"],
            [minimal_analysis, minimal_analysis],
            output_dir=out,
        )
        assert os.path.isfile(path)


class TestOrchestratorComparison:
    def test_run_comparison_with_mock(self, tmp_path):
        from agents.orchestrator import TechTrendOrchestrator

        orch = TechTrendOrchestrator(output_dir=str(tmp_path))
        path = orch.run_comparison_with_mock(
            ["AI", "Blockchain"],
            [AI_MOCK, BLOCKCHAIN_MOCK],
        )
        assert os.path.isfile(path)

    @patch("agents.orchestrator.ResearchAgent")
    @patch("agents.orchestrator.AnalysisAgent")
    def test_run_comparison_calls_agents(self, mock_analyst_cls, mock_researcher_cls, tmp_path):
        from agents.orchestrator import TechTrendOrchestrator

        mock_researcher = MagicMock()
        mock_researcher.research.return_value = "Research data"
        mock_researcher_cls.return_value = mock_researcher

        mock_analyst = MagicMock()
        mock_analyst.analyze.return_value = AI_MOCK
        mock_analyst_cls.return_value = mock_analyst

        orch = TechTrendOrchestrator(output_dir=str(tmp_path))
        path = orch.run_comparison(["Tech A", "Tech B"])

        assert mock_researcher.research.call_count == 2
        assert mock_analyst.analyze.call_count == 2
        assert os.path.isfile(path)


class TestComparisonCLI:
    def test_dry_run_compare(self, tmp_path):
        result = subprocess.run(
            [sys.executable, "main.py", "--dry-run",
             "--compare", "Artificial Intelligence", "Blockchain",
             "--output", str(tmp_path)],
            capture_output=True, text=True,
            cwd=os.path.dirname(os.path.dirname(__file__)),
        )
        assert result.returncode == 0
        assert "COMPARISON" in result.stdout
        assert "Report ready" in result.stdout

    def test_compare_needs_two_techs(self):
        result = subprocess.run(
            [sys.executable, "main.py", "--dry-run", "--compare", "OnlyOne"],
            capture_output=True, text=True,
            cwd=os.path.dirname(os.path.dirname(__file__)),
        )
        assert result.returncode != 0
