"""Tests for agent classes (using mocked API client)."""

from unittest.mock import MagicMock
from agents.researcher import ResearchAgent
from agents.analyst import AnalysisAgent, TechAnalysisResult
from agents.orchestrator import TechTrendOrchestrator
from agents.mock_data import AI_MOCK


class TestResearchAgent:
    """Test ResearchAgent with a mocked Anthropic client."""

    def _make_mock_response(self, text, stop_reason="end_turn"):
        block = MagicMock()
        block.text = text
        block.type = "text"

        response = MagicMock()
        response.content = [block]
        response.stop_reason = stop_reason
        return response

    def test_research_returns_text(self):
        mock_client = MagicMock()
        mock_client.messages.create.return_value = self._make_mock_response(
            "AI is a rapidly growing field."
        )

        agent = ResearchAgent(mock_client)
        result = agent.research("Artificial Intelligence")

        assert "AI" in result
        assert mock_client.messages.create.called

    def test_research_handles_pause_turn(self):
        mock_client = MagicMock()
        mock_client.messages.create.side_effect = [
            self._make_mock_response("Partial...", "pause_turn"),
            self._make_mock_response("Complete AI research.", "end_turn"),
        ]

        agent = ResearchAgent(mock_client)
        result = agent.research("AI")

        assert "Complete" in result
        assert mock_client.messages.create.call_count == 2

    def test_research_uses_web_search_tool(self):
        mock_client = MagicMock()
        mock_client.messages.create.return_value = self._make_mock_response("Result.")

        agent = ResearchAgent(mock_client)
        agent.research("Blockchain")

        call_kwargs = mock_client.messages.create.call_args[1]
        tools = call_kwargs["tools"]
        assert any(t["type"] == "web_search_20260209" for t in tools)

    def test_research_uses_adaptive_thinking(self):
        mock_client = MagicMock()
        mock_client.messages.create.return_value = self._make_mock_response("Result.")

        agent = ResearchAgent(mock_client)
        agent.research("Quantum")

        call_kwargs = mock_client.messages.create.call_args[1]
        assert call_kwargs["thinking"] == {"type": "adaptive"}


class TestAnalysisAgent:
    """Test AnalysisAgent with a mocked Anthropic client."""

    def test_analyze_returns_tech_analysis_result(self):
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.parsed_output = AI_MOCK
        mock_client.messages.parse.return_value = mock_response

        agent = AnalysisAgent(mock_client)
        result = agent.analyze("AI", "Raw research text...")

        assert isinstance(result, TechAnalysisResult)

    def test_analyze_passes_correct_model(self):
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.parsed_output = AI_MOCK
        mock_client.messages.parse.return_value = mock_response

        agent = AnalysisAgent(mock_client, model="claude-sonnet-4-6")
        agent.analyze("AI", "Brief.")

        call_kwargs = mock_client.messages.parse.call_args[1]
        assert call_kwargs["model"] == "claude-sonnet-4-6"

    def test_analyze_uses_structured_output(self):
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.parsed_output = AI_MOCK
        mock_client.messages.parse.return_value = mock_response

        agent = AnalysisAgent(mock_client)
        agent.analyze("AI", "Brief.")

        call_kwargs = mock_client.messages.parse.call_args[1]
        assert call_kwargs["output_format"] == TechAnalysisResult


class TestOrchestrator:
    """Test orchestrator coordination logic."""

    def test_orchestrator_initializes(self):
        orch = TechTrendOrchestrator(api_key="test-key")
        assert orch._researcher is not None
        assert orch._analyst is not None

    def test_orchestrator_full_pipeline(self, tmp_path):
        mock_client = MagicMock()

        research_block = MagicMock()
        research_block.text = "Research about AI technology."
        research_block.type = "text"
        research_response = MagicMock()
        research_response.content = [research_block]
        research_response.stop_reason = "end_turn"
        mock_client.messages.create.return_value = research_response

        analysis_response = MagicMock()
        analysis_response.parsed_output = AI_MOCK
        mock_client.messages.parse.return_value = analysis_response

        orch = TechTrendOrchestrator(output_dir=str(tmp_path))
        orch.client = mock_client
        orch._researcher = ResearchAgent(mock_client)
        orch._analyst = AnalysisAgent(mock_client)

        report_path = orch.run("Artificial Intelligence")
        assert report_path.endswith(".docx")
        assert "artificial_intelligence" in report_path
