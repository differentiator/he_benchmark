import logging
import pathlib
import os
import argparse
import itertools
import json

from benchmarking.runner import Benchmark
from report.generator import ReportGenerator
from utils.validator import str2bool
from utils.logging import logger

import encryption


def dump_results_to_file(data: dict, path: pathlib.Path):
    """
    Save data to path as json
    Args:
        data: dict, with required data
        path: pathlib.Path, to the output file

    Returns:

    """
    with open(path, "w+") as f:
        json.dump(data, f)


def pretty_print(data: dict):
    """
    Pretty print
    Args:
        data: dict

    Returns:
        print of the data with indents
    """
    print(json.dumps(data, indent=4))


def main(args: argparse.Namespace):
    """
    Main entry point of the app
    Args:
        args: argparse.Namespace

    Returns:
        print of the benchmarking result
    """
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    classes = []
    for module in itertools.chain(*args.class_name):
        try:
            imported_class = getattr(encryption, module)
            classes.append(imported_class)
        except AttributeError:
            logger.debug("ERROR: missing python module: " + module + "\n")
    benchmark = Benchmark(encryption_classes=classes, num_runs=args.number_of_runs)
    results = benchmark.run()
    report_gen = ReportGenerator(results)
    report_results = report_gen.generate()
    if args.output_folder:
        # 1. Prepare path for the output
        os.makedirs(args.output_folder, exist_ok=True)
        out_dir = pathlib.Path(args.output_folder)
        raw_path = out_dir / r"raw_results.json"
        aggregated_path = out_dir / r"agg_results.json"
        # 2. Save report and raw data
        dump_results_to_file(results, raw_path)
        dump_results_to_file(report_results, aggregated_path)

    logger.debug(report_results)
    if not args.output_folder or args.verbose:
        pretty_print(report_results)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--number_of_runs", type=int, default=10,
                        help="Number of runs per operation")
    parser.add_argument("-c", "--class_name", action='append', nargs='+',
                        help="Class name of implemented backends, can be multiple")
    parser.add_argument("-o", "--output_folder",
                        default=None,
                        help="Output folder to save results")
    parser.add_argument("-v", "--verbose", type=str2bool,
                        default=False,
                        help="Verbosity for logging")

    args = parser.parse_args()
    main(args)
