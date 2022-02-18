import sys
from getopt import getopt, GetoptError

from api_interface.api_configuration import configure as configure_api
from api_interface.request_engine import RequestEngine

from core.sample_fuzzer import SampleFuzzer

HELP_TEXT = "\n\nInstructions to use:\npython3 fuzz.py -c path/to/api-config.yml\n\n"


def main(argv):
    """
    Driver code to run the fuzzer

    :param argv: list of command-line arguments given
    """

    try:
        opts, args = getopt(argv, 'hc:', ['help', 'api-config'])
    except GetoptError:
        print(HELP_TEXT)
        sys.exit(2)

    api_config_file_path = None
    for opt, arg in opts:
        if opt in ['-c', '--api-config']:
            api_config_file_path = arg
        else:
            print(HELP_TEXT)
            sys.exit(2)

    if not api_config_file_path:
        print(HELP_TEXT)
        sys.exit(2)

    # Generate API Configuration
    configure_api(api_config_file_path)

    SampleFuzzer()


if __name__ == '__main__':
    main(sys.argv[1:])
