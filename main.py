#!/usr/bin/python3

import argparse
import sys

from core.signs import tradeSigns



def getOptions(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="Parses command.")
    parser.add_argument("-s", "--symbol", type=str, help="Stock symbol.")
    parser.add_argument("-t", "--timeframe", type=str, help="Time frame.")
    #parser.add_argument("-v", "--verbose",dest='verbose',action='store_true', help="Verbose mode.")
    options = parser.parse_args(args)
    return options

def run():

    symbol = ""
    timeframe = ""

    getOptions(args=sys.argv[1:])
    options = getOptions(sys.argv[1:])

    if options.symbol:
      symbol = str(options.symbol)
    else:
      symbol = "BTCUSDT"

    
    if options.timeframe:
      timeframe = str(options.timeframe)
    else:
      timeframe = "1h"


    ts = tradeSigns()
    ts.sign(symbol, timeframe)


def main():
    # print command line arguments
  run()



if __name__ == "__main__":
    main()