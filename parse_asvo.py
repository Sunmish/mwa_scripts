#! /usr/bin/env python

import numpy as np
from argparse import ArgumentParser
from astropy.io.votable import parse_single_table


def open_xml(xml):
    """Open .xml file from ASVO."""

    table = parse_single_table(xml).array

    return table


def get_obs(table, source, chan):
    """Get a list of observation IDs for `source` at `chan`."""

    obsids = []
    for i in range(len(table["obs_title"])):
        if table["obs_title"][i].split("_")[-1] == str(chan) and \
            table["obs_title"][i].split("_")[0] == source:
            obsids.append(table["obs_id"][i])

    return obsids


def main():
    """The main function."""

    ps = ArgumentParser(description="Output list of observation IDs given "
                                    "an input VOTable output from the MWA "
                                    "ASVO online archive.")

    ps.add_argument("table", type=str, 
                    help="VOTable (.xml) output from the MWA ASVO archive.")
    ps.add_argument("-s", "--source", type=str, default=None, nargs="*",
                    help="Source/target name, without channel appended. "
                         "Multiple sources can be specified.")
    ps.add_argument("-c", "--chan", type=str, default=None, nargs="*",
                    help="Central channel of observation, appended to target "
                         " name. Multiple channels can be specified.")
    ps.add_argument("-o", "--outname", type=str, default=None, 
                    help="Output file name. By default, the output file name "
                         "is determined from the source name and channel.")

    args = ps.parse_args()
    table = open_xml(args.table)

    for source in args.source:
        for chan in args.chan:

            if args.outname is None:
                outname = "{}_{}.txt".format(source, chan)
            else:
                outname = args.outname

            obsids = get_obs(table=table,
                             source=source,
                             chan=chan)

            with open(outname, "w+") as f:
                for obs in obsids:
                    f.write("{}\n".format(obs))


if __name__ == "__main__":
    main()
