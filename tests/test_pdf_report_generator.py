"""Tests for the PDF report generator."""

import os

import pytest

from agents.mock_data import AI_MOCK, COMPARISON_MOCKS
from utils.pdf_report_generator import (
    _sanitize,
    generate_comparison_pdf_report,
    generate_pdf_report,
)


class TestSanitize:
    def test_replaces_em_dash(self):
        assert _sanitize("foo — bar") == "foo -- bar"

    def test_replaces_smart_quotes(self):
        assert _sanitize("‘hi’ “there”") == "'hi' \"there\""

    def test_replaces_bullet_and_ellipsis(self):
        assert _sanitize("• one… two") == "- one... two"

    def test_replaces_german_umlauts(self):
        assert _sanitize("Über grün — Größe") == "Ueber gruen -- Groesse"

    def test_replaces_euro_sign(self):
        assert _sanitize("Cost: 5€") == "Cost: 5EUR"

    def test_handles_none(self):
        assert _sanitize(None) == ""

    def test_pure_ascii_passes_through(self):
        assert _sanitize("plain ascii") == "plain ascii"

    def test_unknown_unicode_does_not_crash(self):
        # 㐀 is a CJK ideograph — replaced with '?' via errors='replace'
        out = _sanitize("hello 㐀 world")
        assert "hello" in out and "world" in out


class TestGeneratePdfReport:
    def test_returns_existing_path(self, tmp_path):
        path = generate_pdf_report("Artificial Intelligence", AI_MOCK, str(tmp_path))
        assert os.path.isfile(path)
        assert path.endswith(".pdf")

    def test_pdf_has_meaningful_size(self, tmp_path):
        path = generate_pdf_report("Artificial Intelligence", AI_MOCK, str(tmp_path))
        # Cover page + several sections + 2 embedded charts → well over 1 kB
        assert os.path.getsize(path) > 1024

    def test_filename_contains_technology(self, tmp_path):
        path = generate_pdf_report("Quantum Computing", AI_MOCK, str(tmp_path))
        assert "quantum_computing" in os.path.basename(path)

    def test_creates_output_directory(self, tmp_path):
        nested = tmp_path / "nested" / "deeper"
        path = generate_pdf_report("AI", AI_MOCK, str(nested))
        assert os.path.isfile(path)


class TestGenerateComparisonPdfReport:
    def test_returns_existing_path(self, tmp_path):
        techs = list(COMPARISON_MOCKS.keys())[:2]
        analyses = [COMPARISON_MOCKS[t] for t in techs]
        path = generate_comparison_pdf_report(techs, analyses, str(tmp_path))
        assert os.path.isfile(path)
        assert path.endswith(".pdf")

    def test_three_way_comparison(self, tmp_path):
        techs = list(COMPARISON_MOCKS.keys())[:3]
        analyses = [COMPARISON_MOCKS[t] for t in techs]
        path = generate_comparison_pdf_report(techs, analyses, str(tmp_path))
        assert os.path.isfile(path)

    def test_filename_contains_all_technologies(self, tmp_path):
        techs = ["AI", "Blockchain"]
        analyses = [COMPARISON_MOCKS.get(t, AI_MOCK) for t in techs]
        path = generate_comparison_pdf_report(techs, analyses, str(tmp_path))
        name = os.path.basename(path).lower()
        assert "ai" in name and "blockchain" in name

    def test_mismatched_lengths_raise(self, tmp_path):
        with pytest.raises(ValueError):
            generate_comparison_pdf_report(["A", "B"], [AI_MOCK], str(tmp_path))
