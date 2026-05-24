"""
Orchestrator — Coordinates the multi-agent technology trend analysis pipeline.

Manages the sequential flow: Research → Analysis → Report Generation.
"""

import anthropic

from agents.researcher import ResearchAgent
from agents.analyst import AnalysisAgent, TechAnalysisResult
from utils.report_generator import generate_docx_report
from utils.comparison_report import generate_comparison_report
from utils.pdf_report_generator import (
    generate_pdf_report,
    generate_comparison_pdf_report,
)


def _resolve_formats(fmt: str) -> list[str]:
    """Map the public ``format`` argument to the concrete list of writers."""
    fmt = (fmt or "docx").lower()
    if fmt == "both":
        return ["docx", "pdf"]
    if fmt in ("docx", "pdf"):
        return [fmt]
    raise ValueError(f"Unknown report format '{fmt}' (expected: docx, pdf, both)")


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

    def _write_reports(
        self,
        technology: str,
        analysis: TechAnalysisResult,
        formats: list[str],
    ) -> list[str]:
        paths: list[str] = []
        if "docx" in formats:
            paths.append(generate_docx_report(technology, analysis, self.output_dir))
        if "pdf" in formats:
            paths.append(generate_pdf_report(technology, analysis, self.output_dir))
        return paths

    def _write_comparison_reports(
        self,
        technologies: list[str],
        analyses: list[TechAnalysisResult],
        formats: list[str],
    ) -> list[str]:
        paths: list[str] = []
        if "docx" in formats:
            paths.append(generate_comparison_report(technologies, analyses, self.output_dir))
        if "pdf" in formats:
            paths.append(generate_comparison_pdf_report(technologies, analyses, self.output_dir))
        return paths

    def run(self, technology: str, format: str = "docx") -> list[str]:
        """
        Execute the full pipeline for a given technology.

        Args:
            technology: Name of the technology to analyze
            format:     "docx" (default), "pdf", or "both"

        Returns:
            Paths to the generated report files.
        """
        formats = _resolve_formats(format)

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
        print(f"\n[3/3] Generating {' + '.join(f.upper() for f in formats)} report ...")
        paths = self._write_reports(technology, analysis, formats)
        for p in paths:
            print(f"      Report saved: {p}")

        return paths

    def run_comparison(self, technologies: list[str], format: str = "docx") -> list[str]:
        """Run the pipeline for multiple technologies and generate a comparison report."""
        formats = _resolve_formats(format)
        analyses = []
        total = len(technologies)

        for idx, tech in enumerate(technologies, 1):
            print(f"\n{'='*60}")
            print(f"  Analyzing {idx}/{total}: {tech}")
            print(f"{'='*60}")

            print(f"\n[1/2] Researching '{tech}' ...")
            research_brief = self._researcher.research(tech)
            word_count = len(research_brief.split())
            print(f"      Research complete: {word_count:,} words collected.")

            print(f"\n[2/2] Analyzing research data ...")
            analysis = self._analyst.analyze(tech, research_brief)
            print(f"      Analysis complete: "
                  f"{len(analysis.key_players)} key players, "
                  f"{len(analysis.use_cases)} use cases.")
            analyses.append(analysis)

        print(f"\n{'='*60}")
        print(f"  Generating comparison report ({' + '.join(f.upper() for f in formats)}) ...")
        print(f"{'='*60}")

        paths = self._write_comparison_reports(technologies, analyses, formats)
        for p in paths:
            print(f"      Report saved: {p}")
        return paths

    def run_comparison_with_mock(
        self,
        technologies: list[str],
        analyses: list[TechAnalysisResult],
        format: str = "docx",
    ) -> list[str]:
        """Run comparison with pre-built analysis data (for --dry-run)."""
        formats = _resolve_formats(format)
        print(f"\n[DRY RUN] Generating comparison report for: {', '.join(technologies)}")
        paths = self._write_comparison_reports(technologies, analyses, formats)
        for p in paths:
            print(f"      Report saved: {p}")
        return paths

    def run_with_mock(
        self,
        technology: str,
        analysis: TechAnalysisResult,
        format: str = "docx",
    ) -> list[str]:
        """Run the pipeline with pre-built analysis data (for --dry-run)."""
        formats = _resolve_formats(format)
        print(f"\n[1/3] DRY RUN — skipping web research (using mock data)")
        print(f"[2/3] DRY RUN — skipping analysis (using mock data)")

        print(f"\n      Mock data loaded: "
              f"{len(analysis.key_players)} key players, "
              f"{len(analysis.use_cases)} use cases, "
              f"{len(analysis.key_trends)} trends.")

        print(f"\n[3/3] Generating {' + '.join(f.upper() for f in formats)} report ...")
        paths = self._write_reports(technology, analysis, formats)
        for p in paths:
            print(f"      Report saved: {p}")
        return paths
