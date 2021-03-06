"""
Use Case: Analyzing data from logfile (after-the-fact analysis)
  - source: logfile
  x save to logfile
  x realtime graph (short-term)
  - session graph (long-term)
  x realtime analysis
  - after-the-fact analysis
"""
import argparse
from pysleep import *


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(prog='python post-analyze.py',
                                     description='Imports a sleep file and performs after-the-fact data and graphical analysis on it')
    parser.add_argument('-m', '--minimum-value', type=int,
                        help='if provided, will print every entry where movement_value > x to stdout')
    parser.add_argument('-s', '--minimum-sum', type=int,
                        help='if provided, will print every entry where sum of last n entires > x to stdout')
    parser.add_argument('file', help='target sleepfile to perform analysis on')
    args = parser.parse_args()

    # Check user is in the right directory
    if (os.getcwd() != os.path.dirname(os.path.realpath(__file__))):
        log.error("Please cd into the script directory before running it!")
        sys.exit(1)

    graph_with_analyzer = GraphWithAnalyzer(minimum_value=args.minimum_value,
                                            min_movement_sum=args.minimum_sum)
    sleep_reader = InFile(args.file)

    while sleep_reader.is_ready:
        try:
            sleep_entry = sleep_reader.get_next_sleep_entry()
            if sleep_entry:
                graph_with_analyzer.add_entry(sleep_entry)
        except KeyboardInterrupt:
            log.info("Interrupt detected. Quitting")
            sleep_reader.close()
            sys.exit(0)
        except Exception as e:
            log.error("Encountered unexpected exception: %s" % e)
            sleep_reader.close()
            sys.exit(1)

    # Run post-load analysis
    log.info("Loaded %d values" % graph_with_analyzer.num_values_recorded)
    sleep_reader.close()
    graph_with_analyzer.show()

    print 'Press Enter to Quit...'
    raw_input()


if __name__ == "__main__":
    main()
