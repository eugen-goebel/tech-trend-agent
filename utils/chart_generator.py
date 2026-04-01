"""
Chart Generator — Creates matplotlib visualizations for technology trend reports.

Produces in-memory chart images (BytesIO) that can be embedded directly
into DOCX documents via python-docx.
"""

from io import BytesIO

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from agents.analyst import TechAnalysisResult


# ---------------------------------------------------------------------------
# Color palette (matches report theme)
# ---------------------------------------------------------------------------
CHART_DARK_GREEN = "#1A6C3C"
CHART_MED_GREEN = "#2EB46D"
CHART_BG = "#FAFFFE"
CHART_TEXT = "#2D3748"

MARKET_POSITION_SCORES = {
    "market leader": 5, "dominant": 5, "leading": 4, "leader": 4,
    "strongest": 4, "strong": 3, "major": 3, "largest": 4,
    "near-monopoly": 5, "growing": 2, "emerging": 1, "niche": 1,
}


def _estimate_market_relevance(market_position: str) -> int:
    """Derive a 1-5 relevance score from free-text market position descriptions."""
    lower = market_position.lower()
    for keyword, score in MARKET_POSITION_SCORES.items():
        if keyword in lower:
            return score
    return 3


def create_key_players_chart(analysis: TechAnalysisResult) -> BytesIO:
    """
    Create a horizontal bar chart showing key player market relevance.

    Returns:
        BytesIO buffer containing the chart as a PNG image.
    """
    players = analysis.key_players
    if not players:
        return _empty_chart("No key players data available")

    names = [p.name for p in players]
    scores = [_estimate_market_relevance(p.market_position) for p in players]

    fig, ax = plt.subplots(figsize=(6.0, max(2.5, 0.55 * len(players))))
    fig.patch.set_facecolor(CHART_BG)
    ax.set_facecolor(CHART_BG)

    bars = ax.barh(names, scores, color=CHART_MED_GREEN, edgecolor=CHART_DARK_GREEN, linewidth=0.6)

    ax.set_xlim(0, 5.5)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax.set_xlabel("Market Relevance (1-5)", fontsize=9, color=CHART_TEXT)
    ax.set_title("Key Player Market Relevance", fontsize=11, fontweight="bold",
                 color=CHART_DARK_GREEN, pad=10)

    ax.tick_params(axis="both", labelsize=8.5, colors=CHART_TEXT)
    ax.invert_yaxis()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    for bar, score in zip(bars, scores):
        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2,
                str(score), va="center", fontsize=8.5, color=CHART_TEXT)

    fig.tight_layout()
    return _fig_to_buffer(fig)


def create_use_case_impact_chart(analysis: TechAnalysisResult) -> BytesIO:
    """
    Create a bar chart showing use case distribution by impact level.

    Returns:
        BytesIO buffer containing the chart as a PNG image.
    """
    impact_counts = {"High": 0, "Medium": 0, "Low": 0}
    for uc in analysis.use_cases:
        if uc.impact_level in impact_counts:
            impact_counts[uc.impact_level] += 1

    if all(c == 0 for c in impact_counts.values()):
        return _empty_chart("No use case data available")

    levels = list(impact_counts.keys())
    counts = list(impact_counts.values())
    colors = ["#C62828", "#E65100", "#2E7D32"]

    fig, ax = plt.subplots(figsize=(4.5, 3.0))
    fig.patch.set_facecolor(CHART_BG)
    ax.set_facecolor(CHART_BG)

    bars = ax.bar(levels, counts, color=colors, edgecolor="#FFFFFF", linewidth=0.8, width=0.5)

    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax.set_ylabel("Number of Use Cases", fontsize=9, color=CHART_TEXT)
    ax.set_title("Use Cases by Impact Level", fontsize=11, fontweight="bold",
                 color=CHART_DARK_GREEN, pad=10)

    ax.tick_params(axis="both", labelsize=9, colors=CHART_TEXT)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    for bar, count in zip(bars, counts):
        if count > 0:
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                    str(count), ha="center", fontsize=9, fontweight="bold", color=CHART_TEXT)

    fig.tight_layout()
    return _fig_to_buffer(fig)


def _fig_to_buffer(fig) -> BytesIO:
    """Save a matplotlib figure to a BytesIO buffer and close it."""
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=180, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf


def _empty_chart(message: str) -> BytesIO:
    """Create a simple placeholder chart with a message."""
    fig, ax = plt.subplots(figsize=(4, 2))
    ax.text(0.5, 0.5, message, ha="center", va="center", fontsize=10, color="#999999")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    return _fig_to_buffer(fig)
