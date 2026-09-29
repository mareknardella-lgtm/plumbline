import argparse
import json
import sys

from .mutator import generate_mutants
from .runner import check_api_surface, compute_metrics, run_probes, run_tests
from .survey import survey_source


def main():
    parser = argparse.ArgumentParser(prog="plumbline_tools")
    subparsers = parser.add_subparsers(dest="command", required=True)

    survey_parser = subparsers.add_parser("survey")
    survey_parser.add_argument("file")

    mutate_parser = subparsers.add_parser("mutate")
    mutate_parser.add_argument("file")
    mutate_parser.add_argument("--max-count", type=int, default=40)
    mutate_parser.add_argument("--seed", type=int, default=42)

    test_parser = subparsers.add_parser("run-tests")
    test_parser.add_argument("test_dir")
    test_parser.add_argument("source_dir")

    probe_parser = subparsers.add_parser("run-probes")
    probe_parser.add_argument("original")
    probe_parser.add_argument("candidate")
    probe_parser.add_argument("probes_json")

    metrics_parser = subparsers.add_parser("metrics")
    metrics_parser.add_argument("file")

    api_parser = subparsers.add_parser("api-surface")
    api_parser.add_argument("module")

    args = parser.parse_args()

    result = {}

    try:
        if args.command == "survey":
            with open(args.file) as f:
                result = survey_source(f.read())
        elif args.command == "mutate":
            with open(args.file) as f:
                result = generate_mutants(f.read(), args.max_count, args.seed)
        elif args.command == "run-tests":
            result = run_tests(args.test_dir, args.source_dir)
        elif args.command == "run-probes":
            with open(args.probes_json) as f:
                probes = json.load(f)
            result = run_probes(args.original, args.candidate, probes)
        elif args.command == "metrics":
            with open(args.file) as f:
                result = compute_metrics(f.read())
        elif args.command == "api-surface":
            result = check_api_surface(args.module)

        print(json.dumps(result, indent=2))

    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
