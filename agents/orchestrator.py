"""
Orchestrator — Coordinates the multi-agent technology trend analysis pipeline.

Manages the sequential flow: Research → Analysis → Report Generation.
"""

import anthropic

from agents.researcher import ResearchAgent
from agents.analyst import AnalysisAgent, TechAnalysisResult
from utils.report_generator import generate_docx_report


class TechTrendOrchestrator:
    """
    Coordinates the three-phase pipeline for technology trend analysis.

    Phase 1: ResearchAgent gathers web intelligence
    Phase 2: AnalysisAgent produces structured TechAnalysisResult
    Phase 3: ReportGenerator creates professional DOCX output
    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "claude-opus-4-6",
        output_dir: str = "output",
    ):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        self.output_dir = output_dir

        self._researcher = ResearchAgent(self.client, model=model)
        self._analyst = AnalysisAgent(self.client, model=model)

    def run(self, technology: str) -> str:
        """
        Execute the full pipeline for a given technology.

        Args:
            technology: Name of the technology to analyze

        Returns:
            Absolute path to the generated DOCX report
        """
        # Phase 1: Research
        print(f"\n[1/3] Researching '{technology}' — gathering web intelligence ...")
        research_brief = self._researcher.research(technology)
        word_count = len(research_brief.split())
        print(f"      Research complete: {word_count:,} words collected.")

        # Phase 2: Analysis
        print(f"\n[2/3] Analyzing research data — extracting structured insights ...")
        analysis = self._analyst.analyze(technology, research_brief)
        print(
            f"      Analysis complete: "
            f"{len(analysis.key_players)} key players, "
            f"{len(analysis.use_cases)} use cases, "
            f"{len(analysis.key_trends)} trends identified."
        )

        # Phase 3: Report
        print(f"\n[3/3] Generating DOCX report ...")
        report_path = generate_docx_report(technology, analysis, self.output_dir)
        print(f"      Report saved: {report_path}")

        return report_path

    def run_with_mock(self, technology: str, analysis: TechAnalysisResult) -> str:
        """
        Run the pipeline with pre-built analysis data (for --dry-run).

        Args:
            technology: Technology name for the report title
            analysis:   Pre-built TechAnalysisResult

        Returns:
            Absolute path to the generated DOCX report
        """
        print(f"\n[1/3] DRY RUN — skipping web research (using mock data)")
        print(f"[2/3] DRY RUN — skipping analysis (using mock data)")

        print(f"\n      Mock data loaded: "
              f"{len(analysis.key_players)} key players, "
              f"{len(analysis.use_cases)} use cases, "
              f"{len(analysis.key_trends)} trends.")

        print(f"\n[3/3] Generating DOCX report ...")
        report_path = generate_docx_report(technology, analysis, self.output_dir)
        print(f"      Report saved: {report_path}")

        return report_path
