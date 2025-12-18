"""
Console output formatter for benchmark results.

Displays benchmark results as a formatted table in the terminal
using the tabulate library for clean presentation.

Author: SpeedyFibonacci Contributors
License: MIT
"""

import sys
import os
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from tabulate import tabulate
    TABULATE_AVAILABLE = True
except ImportError:
    TABULATE_AVAILABLE = False

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


class ConsoleFormatter:
    """
    Formats and displays benchmark results in the console.

    Supports multiple output styles:
    - Rich tables (colored, styled) if rich is available
    - Tabulate tables (clean ASCII) if tabulate is available
    - Basic fallback if neither is available
    """

    def __init__(self, use_rich: bool = True):
        """
        Initialize the formatter.

        Args:
            use_rich: Prefer rich library for colored output (default: True)
        """
        self.use_rich = use_rich and RICH_AVAILABLE

    def display(self, summary) -> None:
        """
        Display benchmark results.

        Args:
            summary: BenchmarkSummary object with results
        """
        if self.use_rich:
            self._display_rich(summary)
        elif TABULATE_AVAILABLE:
            self._display_tabulate(summary)
        else:
            self._display_basic(summary)

    def _display_rich(self, summary) -> None:
        """Display using rich library for colored output."""
        console = Console()

        # Header
        console.print()
        console.print(Panel.fit(
            "[bold cyan]SpeedyFibonacci Benchmark Results[/bold cyan]",
            border_style="cyan"
        ))
        console.print()

        # Results table
        table = Table(
            title="Fibonacci Calculation Performance (1 second each)",
            show_header=True,
            header_style="bold magenta"
        )

        table.add_column("Rank", style="dim", width=4)
        table.add_column("Technique", style="cyan", width=28)
        table.add_column("Numbers Calculated", justify="right", style="green")
        table.add_column("Max N", justify="right", style="yellow")
        table.add_column("Time", justify="center", width=10)
        table.add_column("Space", justify="center", width=10)
        table.add_column("Status", justify="center", width=8)

        # Sort by count (descending)
        sorted_results = summary.get_sorted_by_count(descending=True)

        for rank, result in enumerate(sorted_results, 1):
            status = "[green]OK[/green]" if result.success else f"[red]{result.error[:20]}[/red]"

            # Color code the count based on performance
            if rank <= 3:
                count_style = "bold green"
            elif rank <= 6:
                count_style = "green"
            else:
                count_style = "white"

            table.add_row(
                str(rank),
                result.technique_name,
                f"[{count_style}]{result.count:,}[/{count_style}]",
                f"{result.max_n:,}",
                result.time_complexity,
                result.space_complexity,
                status
            )

        console.print(table)

        # Summary stats
        console.print()
        fastest = summary.get_fastest()
        highest = summary.get_highest_n()

        if fastest:
            console.print(f"[bold]Fastest:[/bold] {fastest.technique_name} "
                         f"({fastest.count:,} numbers)")
        if highest:
            console.print(f"[bold]Highest N:[/bold] {highest.technique_name} "
                         f"(reached n={highest.max_n:,})")

        console.print(f"\n[dim]Total benchmark time: {summary.total_duration:.2f}s[/dim]")

    def _display_tabulate(self, summary) -> None:
        """Display using tabulate library."""
        print()
        print("=" * 80)
        print("  SpeedyFibonacci Benchmark Results")
        print("  Fibonacci Calculation Performance (1 second each)")
        print("=" * 80)
        print()

        # Prepare table data
        headers = ["Rank", "Technique", "Count", "Max N", "Time O()", "Space O()", "Status"]
        rows = []

        sorted_results = summary.get_sorted_by_count(descending=True)

        for rank, result in enumerate(sorted_results, 1):
            status = "OK" if result.success else "ERROR"
            rows.append([
                rank,
                result.technique_name,
                f"{result.count:,}",
                f"{result.max_n:,}",
                result.time_complexity,
                result.space_complexity,
                status
            ])

        print(tabulate(rows, headers=headers, tablefmt="rounded_grid"))

        # Summary
        print()
        fastest = summary.get_fastest()
        highest = summary.get_highest_n()

        if fastest:
            print(f"Fastest: {fastest.technique_name} ({fastest.count:,} numbers)")
        if highest:
            print(f"Highest N: {highest.technique_name} (reached n={highest.max_n:,})")

        print(f"\nTotal benchmark time: {summary.total_duration:.2f}s")

    def _display_basic(self, summary) -> None:
        """Basic display without external libraries."""
        print()
        print("=" * 80)
        print("  SpeedyFibonacci Benchmark Results")
        print("=" * 80)
        print()

        # Header
        print(f"{'Rank':<5} {'Technique':<30} {'Count':>15} {'Max N':>12} {'Status':<8}")
        print("-" * 80)

        sorted_results = summary.get_sorted_by_count(descending=True)

        for rank, result in enumerate(sorted_results, 1):
            status = "OK" if result.success else "ERROR"
            print(f"{rank:<5} {result.technique_name:<30} {result.count:>15,} "
                  f"{result.max_n:>12,} {status:<8}")

        print("-" * 80)

        # Summary
        fastest = summary.get_fastest()
        highest = summary.get_highest_n()

        if fastest:
            print(f"\nFastest: {fastest.technique_name} ({fastest.count:,} numbers)")
        if highest:
            print(f"Highest N: {highest.technique_name} (reached n={highest.max_n:,})")

        print(f"\nTotal benchmark time: {summary.total_duration:.2f}s")

    def format_as_string(self, summary) -> str:
        """
        Format results as a string.

        Args:
            summary: BenchmarkSummary object

        Returns:
            Formatted string representation
        """
        lines = []
        lines.append("SpeedyFibonacci Benchmark Results")
        lines.append("=" * 50)
        lines.append("")

        sorted_results = summary.get_sorted_by_count(descending=True)

        for rank, result in enumerate(sorted_results, 1):
            lines.append(f"{rank}. {result.technique_name}")
            lines.append(f"   Count: {result.count:,}")
            lines.append(f"   Max N: {result.max_n:,}")
            lines.append(f"   Complexity: {result.time_complexity} time, "
                        f"{result.space_complexity} space")
            lines.append("")

        return "\n".join(lines)
