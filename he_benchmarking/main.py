import time
import argparse
import itertools
from benchmarking.runner import Benchmark

from utils.validator import str2bool
import encryption


def main(args):
    """ Main entry point of the app """
    classes = []
    for module in itertools.chain(*args.class_names):
        try:
            imported_class = getattr(encryption, module)
            classes.append(imported_class)
        except AttributeError:
            print("ERROR: missing python module: " + module + "\n")
    benchmark = Benchmark(encryption_classes=classes, num_runs=args.number_of_runs)
    results = benchmark.run()
    print(results)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--number_of_runs", type=int, default=10,
                        help="Number of runs per operation")
    parser.add_argument("-c", "--class_names", action='append', nargs='+',
                        help="Class names of implemented backends")
    parser.add_argument("-v", "--verbose", type=str2bool,
                        const=True, default=False,
                        help="Verbosity for logging")

    args = parser.parse_args()
    main(args)
