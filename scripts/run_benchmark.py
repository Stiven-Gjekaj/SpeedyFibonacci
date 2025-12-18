#!/usr/bin/env python3
"""
SpeedyFibonacci Benchmark Runner

Main entry point for running Fibonacci technique benchmarks.
Compares all implemented techniques, measuring how many Fibonacci
numbers each can calculate in one second.

Usage:
    python scripts/run_benchmark.py [options]

Options:
    --duration SECONDS    Duration for each technique (default: 1.0)
    --output-dir DIR      Directory for results (default: results/)
    --no-plots            Skip generating visualization plots
    --no-csv              Skip CSV export
    --quiet               Minimal output
    --technique NAME      Run only specific technique(s)

Example:
    python scripts/run_benchmark.py
    python scripts/run_benchmark.py --duration 5
    python scripts/run_benchmark.py --no-plots --technique "Naive Recursion"

Author: SpeedyFibonacci Contributors
License: MIT
"""

import argparse
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from benchmarking.benchmark_runner import BenchmarkRunner
from benchmarking.technique_loader import load_all_techniques, get_technique_by_name
from output.console_formatter import ConsoleFormatter
from output.csv_exporter import CSVExporter
from output.visualizer import Visualizer


def print_banner():
    """Print the SpeedyFibonacci banner."""
    banner = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   ███████╗██████╗ ███████╗███████╗██████╗ ██╗   ██╗           ║
║   ██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗╚██╗ ██╔╝           ║
║   ███████╗██████╔╝█████╗  █████╗  ██║  ██║ ╚████╔╝            ║
║   ╚════██║██╔═══╝ ██╔══╝  ██╔══╝  ██║  ██║  ╚██╔╝             ║
║   ███████║██║     ███████╗███████╗██████╔╝   ██║              ║
║   ╚══════╝╚═╝     ╚══════╝╚══════╝╚═════╝    ╚═╝              ║
║                                                               ║
║   ███████╗██╗██████╗  ██████╗ ███╗   ██╗ █████╗  ██████╗██╗   ║
║   ██╔════╝██║██╔══██╗██╔═══██╗████╗  ██║██╔══██╗██╔════╝██║   ║
║   █████╗  ██║██████╔╝██║   ██║██╔██╗ ██║███████║██║     ██║   ║
║   ██╔══╝  ██║██╔══██╗██║   ██║██║╚██╗██║██╔══██║██║     ██║   ║
║   ██║     ██║██████╔╝╚██████╔╝██║ ╚████║██║  ██║╚██████╗██║   ║
║   ╚═╝     ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝╚═╝   ║
║                                                               ║
║   Fibonacci Calculation Benchmark Suite                       ║
║   Comparing 12 different techniques                           ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
"""
    print(banner)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="SpeedyFibonacci Benchmark Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/run_benchmark.py
  python scripts/run_benchmark.py --duration 5
  python scripts/run_benchmark.py --no-plots
  python scripts/run_benchmark.py --technique "Naive Recursion"
        """
    )

    parser.add_argument(
        '--duration', '-d',
        type=float,
        default=1.0,
        help='Duration to run each technique (seconds, default: 1.0)'
    )

    parser.add_argument(
        '--output-dir', '-o',
        type=Path,
        default=project_root / 'results',
        help='Output directory for results (default: results/)'
    )

    parser.add_argument(
        '--no-plots',
        action='store_true',
        help='Skip generating visualization plots'
    )

    parser.add_argument(
        '--no-csv',
        action='store_true',
        help='Skip CSV export'
    )

    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Minimal output (no banner, progress only)'
    )

    parser.add_argument(
        '--technique', '-t',
        action='append',
        help='Run only specific technique(s) by name (can be repeated)'
    )

    parser.add_argument(
        '--list',
        action='store_true',
        help='List available techniques and exit'
    )

    parser.add_argument(
        '--no-validate',
        action='store_true',
        help='Skip result validation (faster but no correctness check)'
    )

    args = parser.parse_args()

    # List techniques and exit
    if args.list:
        print("Available Fibonacci techniques:")
        print("-" * 40)
        techniques = load_all_techniques(validate=False)
        for i, tech in enumerate(techniques, 1):
            print(f"{i:2}. {tech.name}")
            print(f"    {tech.description}")
            print(f"    Time: {tech.time_complexity}, Space: {tech.space_complexity}")
            print()
        return 0

    # Print banner
    if not args.quiet:
        print_banner()

    # Filter techniques if specified
    techniques = None
    if args.technique:
        techniques = []
        all_techniques = load_all_techniques(validate=False)
        for name in args.technique:
            found = False
            for tech in all_techniques:
                if tech.name.lower() == name.lower():
                    techniques.append(tech)
                    found = True
                    break
            if not found:
                print(f"Warning: Technique '{name}' not found")

        if not techniques:
            print("Error: No valid techniques specified")
            return 1

    # Initialize runner
    runner = BenchmarkRunner(
        duration=args.duration,
        validate=not args.no_validate,
        verbose=not args.quiet
    )

    # Run benchmarks
    if not args.quiet:
        print(f"\nBenchmark Configuration:")
        print(f"  Duration per technique: {args.duration}s")
        print(f"  Output directory: {args.output_dir}")
        print(f"  Validation: {'disabled' if args.no_validate else 'enabled'}")
        print()

    summary = runner.run_all(techniques=techniques)

    # Display results
    formatter = ConsoleFormatter()
    formatter.display(summary)

    # Export CSV
    if not args.no_csv:
        csv_exporter = CSVExporter(output_dir=args.output_dir)
        csv_path = csv_exporter.export(summary)
        print(f"\nResults exported to: {csv_path}")

        # Also export plotting-friendly format
        plot_csv = csv_exporter.export_for_plotting(summary)
        print(f"Plot data exported to: {plot_csv}")

    # Generate plots
    if not args.no_plots:
        visualizer = Visualizer(output_dir=args.output_dir)
        plot_files = visualizer.generate_plots(summary)
        if plot_files:
            print(f"\nGenerated {len(plot_files)} visualization(s):")
            for pf in plot_files:
                print(f"  - {pf}")
        else:
            print("\nNote: Install matplotlib for visualization plots")

    print("\nBenchmark complete!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
