"""
CSV export functionality for benchmark results.

Exports benchmark results to CSV format for further analysis
in spreadsheets or data analysis tools.

Author: SpeedyFibonacci Contributors
License: MIT
"""

import csv
import sys
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class CSVExporter:
    """
    Exports benchmark results to CSV files.

    CSV format includes:
    - Technique name and description
    - Numbers calculated (count)
    - Maximum n reached
    - Time and space complexity
    - Benchmark timestamp
    """

    def __init__(self, output_dir: Optional[Path] = None):
        """
        Initialize the CSV exporter.

        Args:
            output_dir: Directory for output files (default: results/)
        """
        if output_dir is None:
            output_dir = Path(__file__).parent.parent / "results"
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export(self, summary, filename: Optional[str] = None) -> Path:
        """
        Export benchmark results to CSV.

        Args:
            summary: BenchmarkSummary object with results
            filename: Custom filename (default: timestamped)

        Returns:
            Path to the created CSV file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"benchmark_results_{timestamp}.csv"

        filepath = self.output_dir / filename

        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

            # Header row
            writer.writerow([
                'rank',
                'technique',
                'description',
                'count',
                'max_n',
                'time_complexity',
                'space_complexity',
                'duration_seconds',
                'rate_per_second',
                'success',
                'error',
                'timestamp'
            ])

            # Data rows (sorted by count)
            sorted_results = summary.get_sorted_by_count(descending=True)

            for rank, result in enumerate(sorted_results, 1):
                writer.writerow([
                    rank,
                    result.technique_name,
                    result.description,
                    result.count,
                    result.max_n,
                    result.time_complexity,
                    result.space_complexity,
                    f"{result.duration:.4f}",
                    f"{result.rate:.2f}",
                    result.success,
                    result.error or '',
                    result.timestamp.isoformat()
                ])

        return filepath

    def export_summary(self, summary, filename: Optional[str] = None) -> Path:
        """
        Export a summary CSV with aggregated statistics.

        Args:
            summary: BenchmarkSummary object
            filename: Custom filename (default: timestamped)

        Returns:
            Path to the created CSV file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"benchmark_summary_{timestamp}.csv"

        filepath = self.output_dir / filename

        fastest = summary.get_fastest()
        highest = summary.get_highest_n()

        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

            writer.writerow(['metric', 'value'])
            writer.writerow(['total_techniques', len(summary.results)])
            writer.writerow(['total_duration_seconds', f"{summary.total_duration:.2f}"])
            writer.writerow(['benchmark_timestamp', summary.timestamp.isoformat()])

            if fastest:
                writer.writerow(['fastest_technique', fastest.technique_name])
                writer.writerow(['fastest_count', fastest.count])

            if highest:
                writer.writerow(['highest_n_technique', highest.technique_name])
                writer.writerow(['highest_n_value', highest.max_n])

            # Success rate
            successful = sum(1 for r in summary.results if r.success)
            writer.writerow(['successful_techniques', successful])
            writer.writerow(['failed_techniques', len(summary.results) - successful])

        return filepath

    def export_for_plotting(self, summary, filename: Optional[str] = None) -> Path:
        """
        Export CSV optimized for plotting tools.

        Args:
            summary: BenchmarkSummary object
            filename: Custom filename

        Returns:
            Path to the created CSV file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"benchmark_plot_data_{timestamp}.csv"

        filepath = self.output_dir / filename

        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

            writer.writerow(['technique', 'count', 'max_n', 'complexity_class'])

            for result in summary.get_sorted_by_count(descending=True):
                # Classify complexity for grouping in plots
                complexity = result.time_complexity.lower()
                if 'log' in complexity:
                    complexity_class = 'logarithmic'
                elif '2^n' in complexity or 'exponential' in complexity:
                    complexity_class = 'exponential'
                elif 'n' in complexity:
                    complexity_class = 'linear'
                else:
                    complexity_class = 'constant'

                writer.writerow([
                    result.technique_name,
                    result.count,
                    result.max_n,
                    complexity_class
                ])

        return filepath
