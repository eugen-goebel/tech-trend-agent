"""
Tech Trend Report Agent — CLI entry point.

Generates comprehensive technology trend reports using a multi-agent
pipeline: web research, structured analysis, and DOCX generation.
"""

import argparse
import os
import sys

from dotenv import load_dotenv


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="Generate AI-powered technology trend reports"
    )
    parser.add_argument(
        "technology",
        nargs="?",
        default="Artificial Intelligence",
        help="Technology to analyze (e.g., 'Quantum Computing', 'Blockchain')",
    )
    parser.add_argument(
        "--compare",
        nargs="+",
        metavar="TECH",
        help="Compare 2-3 technologies side-by-side (e.g., --compare 'AI' 'Blockchain')",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run with sample data (no API key needed)",
    )
    parser.add_argument(
        "--output",
        default="output",
        help="Output directory for reports (default: output/)",
    )
    parser.add_argument(
        "--model",
        default="claude-opus-4-6",
        help="Model to use for analysis (default: claude-opus-4-6)",
    )

    args = parser.parse_args()

    if args.compare and len(args.compare) < 2:
        print("Error: --compare requires at least 2 technologies.")
        sys.exit(1)
    if args.compare and len(args.compare) > 3:
        print("Error: --compare supports at most 3 technologies.")
        sys.exit(1)

    if args.dry_run:
        from agents.mock_data import AI_MOCK, COMPARISON_MOCKS
        from agents.orchestrator import TechTrendOrchestrator

        orch = TechTrendOrchestrator(output_dir=args.output)

        if args.compare:
            techs = args.compare
            analyses = [COMPARISON_MOCKS.get(t, AI_MOCK) for t in techs]
            print("=" * 60)
            print(f"  TECH COMPARISON REPORT — DRY RUN")
            print(f"  Technologies: {', '.join(techs)}")
            print("=" * 60)
            report_path = orch.run_comparison_with_mock(techs, analyses)
        else:
            print("=" * 60)
            print(f"  TECH TREND REPORT — DRY RUN")
            print(f"  Technology: {args.technology}")
            print("=" * 60)
            report_path = orch.run_with_mock(args.technology, AI_MOCK)

        print("\n" + "=" * 60)
        print(f"  Report ready: {report_path}")
        print("=" * 60)
    else:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            print("Error: ANTHROPIC_API_KEY not set.")
            print("Set it via .env file or environment variable.")
            print("Or use --dry-run to test without an API key.")
            sys.exit(1)

        from agents.orchestrator import TechTrendOrchestrator

        orch = TechTrendOrchestrator(
            api_key=api_key,
            model=args.model,
            output_dir=args.output,
        )

        if args.compare:
            techs = args.compare
            print("=" * 60)
            print(f"  TECH COMPARISON REPORT")
            print(f"  Technologies: {', '.join(techs)}")
            print("=" * 60)
            report_path = orch.run_comparison(techs)
        else:
            print("=" * 60)
            print(f"  TECH TREND REPORT")
            print(f"  Technology: {args.technology}")
            print("=" * 60)
            report_path = orch.run(args.technology)

        print("\n" + "=" * 60)
        print(f"  Report ready: {report_path}")
        print("=" * 60)


if __name__ == "__main__":
    main()
