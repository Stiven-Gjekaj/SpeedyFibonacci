"""
Visualization module for benchmark results.

Generates matplotlib plots comparing Fibonacci technique performance.

Author: SpeedyFibonacci Contributors
License: MIT
"""

import sys
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


class Visualizer:
    """
    Generates visualization plots for benchmark results.

    Creates three main visualizations:
    1. Bar chart of numbers calculated per technique
    2. Bar chart of maximum n reached per technique
    3. Comparison grouped by complexity class
    """

    def __init__(self, output_dir: Optional[Path] = None):
        """
        Initialize the visualizer.

        Args:
            output_dir: Directory for output files (default: results/)
        """
        if output_dir is None:
            output_dir = Path(__file__).parent.parent / "results"
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Color scheme
        self.colors = {
            'exponential': '#e74c3c',   # Red
            'linear': '#3498db',         # Blue
            'logarithmic': '#2ecc71',    # Green
            'constant': '#9b59b6',       # Purple
        }

    def generate_plots(self, summary, prefix: Optional[str] = None) -> list[Path]:
        """
        Generate all visualization plots.

        Args:
            summary: BenchmarkSummary object
            prefix: Filename prefix (default: timestamp)

        Returns:
            List of paths to generated plot files
        """
        if not MATPLOTLIB_AVAILABLE:
            print("Warning: matplotlib not available. Skipping visualizations.")
            return []

        if prefix is None:
            prefix = datetime.now().strftime("%Y%m%d_%H%M%S")

        plot_files = []

        # Generate each plot
        plot_files.append(self._plot_count_comparison(summary, prefix))
        plot_files.append(self._plot_max_n_comparison(summary, prefix))
        plot_files.append(self._plot_complexity_comparison(summary, prefix))

        return plot_files

    def _get_complexity_class(self, time_complexity: str) -> str:
        """Classify time complexity into categories."""
        complexity = time_complexity.lower()
        if '2^n' in complexity or 'exponential' in complexity:
            return 'exponential'
        elif 'log' in complexity:
            return 'logarithmic'
        elif 'n' in complexity:
            return 'linear'
        else:
            return 'constant'

    def _plot_count_comparison(self, summary, prefix: str) -> Path:
        """Create bar chart of numbers calculated."""
        fig, ax = plt.subplots(figsize=(14, 8))

        sorted_results = summary.get_sorted_by_count(descending=True)

        techniques = [r.technique_name for r in sorted_results]
        counts = [r.count for r in sorted_results]
        colors = [self.colors[self._get_complexity_class(r.time_complexity)]
                  for r in sorted_results]

        bars = ax.barh(techniques, counts, color=colors, edgecolor='black', linewidth=0.5)

        # Add value labels
        for bar, count in zip(bars, counts):
            width = bar.get_width()
            ax.annotate(f'{count:,}',
                       xy=(width, bar.get_y() + bar.get_height()/2),
                       xytext=(5, 0),
                       textcoords='offset points',
                       ha='left', va='center',
                       fontsize=9)

        ax.set_xlabel('Fibonacci Numbers Calculated in 1 Second', fontsize=12)
        ax.set_title('SpeedyFibonacci: Numbers Calculated per Technique', fontsize=14, fontweight='bold')
        ax.invert_yaxis()  # Highest at top

        # Format x-axis with commas
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor=self.colors['exponential'], label='O(2^n) Exponential'),
            Patch(facecolor=self.colors['linear'], label='O(n) Linear'),
            Patch(facecolor=self.colors['logarithmic'], label='O(log n) Logarithmic'),
            Patch(facecolor=self.colors['constant'], label='O(1) Constant'),
        ]
        ax.legend(handles=legend_elements, loc='lower right')

        plt.tight_layout()

        filepath = self.output_dir / f"{prefix}_count_comparison.png"
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()

        return filepath

    def _plot_max_n_comparison(self, summary, prefix: str) -> Path:
        """Create bar chart of maximum n reached."""
        fig, ax = plt.subplots(figsize=(14, 8))

        sorted_results = summary.get_sorted_by_max_n(descending=True)

        techniques = [r.technique_name for r in sorted_results]
        max_ns = [r.max_n for r in sorted_results]
        colors = [self.colors[self._get_complexity_class(r.time_complexity)]
                  for r in sorted_results]

        bars = ax.barh(techniques, max_ns, color=colors, edgecolor='black', linewidth=0.5)

        # Add value labels
        for bar, max_n in zip(bars, max_ns):
            width = bar.get_width()
            ax.annotate(f'{max_n:,}',
                       xy=(width, bar.get_y() + bar.get_height()/2),
                       xytext=(5, 0),
                       textcoords='offset points',
                       ha='left', va='center',
                       fontsize=9)

        ax.set_xlabel('Maximum N Reached', fontsize=12)
        ax.set_title('SpeedyFibonacci: Maximum Fibonacci Index Reached', fontsize=14, fontweight='bold')
        ax.invert_yaxis()

        ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor=self.colors['exponential'], label='O(2^n) Exponential'),
            Patch(facecolor=self.colors['linear'], label='O(n) Linear'),
            Patch(facecolor=self.colors['logarithmic'], label='O(log n) Logarithmic'),
            Patch(facecolor=self.colors['constant'], label='O(1) Constant'),
        ]
        ax.legend(handles=legend_elements, loc='lower right')

        plt.tight_layout()

        filepath = self.output_dir / f"{prefix}_max_n_comparison.png"
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()

        return filepath

    def _plot_complexity_comparison(self, summary, prefix: str) -> Path:
        """Create grouped bar chart by complexity class."""
        fig, ax = plt.subplots(figsize=(12, 6))

        # Group results by complexity
        groups = {'exponential': [], 'linear': [], 'logarithmic': [], 'constant': []}

        for result in summary.results:
            complexity_class = self._get_complexity_class(result.time_complexity)
            groups[complexity_class].append(result)

        # Calculate average count per group
        group_names = []
        avg_counts = []
        group_colors = []
        technique_counts = []

        for class_name in ['logarithmic', 'linear', 'constant', 'exponential']:
            if groups[class_name]:
                group_names.append(f"O({class_name[:3]}...)" if len(class_name) > 5
                                  else f"O({class_name})")
                avg = sum(r.count for r in groups[class_name]) / len(groups[class_name])
                avg_counts.append(avg)
                group_colors.append(self.colors[class_name])
                technique_counts.append(len(groups[class_name]))

        bars = ax.bar(group_names, avg_counts, color=group_colors,
                     edgecolor='black', linewidth=0.5)

        # Add value labels
        for bar, count, tech_count in zip(bars, avg_counts, technique_counts):
            height = bar.get_height()
            ax.annotate(f'{int(count):,}\n({tech_count} techniques)',
                       xy=(bar.get_x() + bar.get_width()/2, height),
                       xytext=(0, 5),
                       textcoords='offset points',
                       ha='center', va='bottom',
                       fontsize=10)

        ax.set_ylabel('Average Numbers Calculated', fontsize=12)
        ax.set_title('SpeedyFibonacci: Performance by Complexity Class',
                    fontsize=14, fontweight='bold')

        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

        plt.tight_layout()

        filepath = self.output_dir / f"{prefix}_complexity_comparison.png"
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()

        return filepath

    def show_plots(self, summary) -> None:
        """
        Display plots interactively (for Jupyter/interactive use).

        Args:
            summary: BenchmarkSummary object
        """
        if not MATPLOTLIB_AVAILABLE:
            print("matplotlib not available")
            return

        # This would display plots in a notebook or interactive session
        # For CLI, we save to files instead
        self.generate_plots(summary)
