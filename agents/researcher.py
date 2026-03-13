"""
Research Agent — Gathers technology trend intelligence from the web.

Uses the server-side web_search tool to find current information about
a given technology, handling multi-turn search continuations automatically.
"""

import anthropic


class ResearchAgent:
    """
    Conducts web-based research on a technology topic using the
    Anthropic server-side search tool.
    """

    def __init__(self, client: anthropic.Anthropic, model: str = "claude-opus-4-6"):
        self.client = client
        self.model = model

    def research(self, technology: str) -> str:
        """
        Run a multi-turn web research session about a technology.

        Args:
            technology: Name of the technology to research

        Returns:
            Concatenated research findings as plain text
        """
        system_prompt = (
            "You are a technology research specialist. Search the web for comprehensive, "
            "up-to-date information about the given technology. Cover:\n"
            "1. What the technology is and how it works\n"
            "2. Current maturity and adoption stage\n"
            "3. Market size and growth projections\n"
            "4. Major companies and organizations involved\n"
            "5. Real-world use cases across industries\n"
            "6. Technical strengths and current limitations\n"
            "7. Factors driving and hindering adoption\n"
            "8. Recent breakthroughs and key trends\n"
            "9. Future outlook and predictions\n"
            "10. Risks and challenges\n\n"
            "Provide concrete data points, statistics, and examples where possible. "
            "Cite specific companies, products, and market figures."
        )

        messages = [
            {
                "role": "user",
                "content": (
                    f"Research the technology '{technology}' thoroughly. "
                    f"Find current market data, key players, use cases, trends, "
                    f"and future outlook. Be specific with numbers and examples."
                ),
            }
        ]

        collected_text: list[str] = []
        max_continuations = 5

        for _ in range(max_continuations + 1):
            response = self.client.messages.create(
                model=self.model,
                max_tokens=16000,
                thinking={"type": "adaptive"},
                system=system_prompt,
                tools=[{"type": "web_search_20260209"}],
                messages=messages,
            )

            for block in response.content:
                if hasattr(block, "text"):
                    collected_text.append(block.text)

            if response.stop_reason != "pause_turn":
                break

            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": "Continue your research."})

        return "\n\n".join(collected_text)
