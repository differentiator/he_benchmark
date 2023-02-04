import time
import argparse
import itertools
import json
from benchmarking.runner import Benchmark

from utils.validator import str2bool
import encryption


# operations that can be compared at the moment are encryption and decryption, sum, multipliation and dot product.
# Then, save and restoring (be carefull, this operation have to be executed and benchamarked toghether because the output of the first function differs)
# the mentioned operation work for both int and float
# WAITING FOR --> RELINEARIZATION
# POSSIBLE SOLUTIONS --> 1. include in all the operations in Pyfhel that require a relinearization (i think just mult and dot) a relinearization so to have a fair comparison
#                        2. find a way to relinearize manually in TENSeal
#                        3. ignore the problem because I don't want to work on Data Security anymore :)

def pretty_print(data):
    print(json.dumps(data, indent=4))


def main(args):
    """ Main entry point of the app """
    classes = []
    for module in itertools.chain(*args.class_name):
        try:
            imported_class = getattr(encryption, module)
            classes.append(imported_class)
        except AttributeError:
            print("ERROR: missing python module: " + module + "\n")
    benchmark = Benchmark(encryption_classes=classes, num_runs=args.number_of_runs)
    results = benchmark.run()
    pretty_print(results)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--number_of_runs", type=int, default=10,
                        help="Number of runs per operation")
    parser.add_argument("-c", "--class_name", action='append', nargs='+',
                        help="Class name of implemented backends, can be multiple")
    parser.add_argument("-v", "--verbose", type=str2bool,
                        default=False,
                        help="Verbosity for logging")

    args = parser.parse_args()
    main(args)
