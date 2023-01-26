import argparse


def main(args):
    """ Main entry point of the app """
    print("hello world")
    print(args)

""" 
    1. Addition of integers/floats
    2. Multiplication of integers/floats
    3. Encryption of integers/floats
    4. Decryption of integers/floats
    5. Substraction / Division test whether to include them
    6. Measure non-linear functions approximation
    7. SCALAR PRODUCT
    8. Saving/Restoring
    9. Relinearization 
    
    Checks for:
    1. Data loss
    2. Data integrity
    3. Decryption precision
"""

if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()
    # 1. Number of runs
    # 2. Timeout in minutes or seconds
    # Required positional argument
    parser.add_argument("arg", help="Required positional argument")

    # Optional argument flag which defaults to False
    parser.add_argument("-f", "--flag", action="store_true", default=False)

    # Optional argument which requires a parameter (eg. -d test)
    parser.add_argument("-n", "--name", action="store", dest="name")

    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Verbosity (-v, -vv, etc)")

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=""))

    args = parser.parse_args()
    main(args)