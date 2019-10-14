#! /usr/bin/env python

from __future__ import print_function, division

import numpy as np
from argparse import ArgumentParser
from astropy.io.votable import parse_single_table


def open_xml(xml):
    """Open .xml file from ASVO."""

    table = parse_single_table(xml).array

    return table


def get_obs(table, source, chan):
    """Get a list of observation IDs for `source` at `chan`."""

    obsids, fov, ra, dec = [], [], [], []
    for i in range(len(table["obs_title"])):

        name = "_".join(table["obs_title"][i].split("_")[:-1])
        channel = table["obs_title"][i].split("_")[-1]

        if channel == str(chan) and \
            name == source:
            obsids.append(table["obs_id"][i])
            fov.append(table["s_fov"][i])
            ra.append(table["s_ra"][i])
            dec.append(table["s_dec"][i])


    return obsids, fov, ra, dec



def region_formatter(name, fov, ra, dec, color="green"):
    """Create a region file."""

    with open(name, "w+") as f:
        f.write("# Region file format: DS9 version 4.1\n")
        f.write("global color={} dashlist=8 3 width=1 font=\"helvetica 10 "
                "normal roman\" select=1 highlite=1 dash=0 fixed=0 edit=1 "
                "move=1 delete=1 include=1 source=1\n".format(color))
        f.write("fk5\n")

        for i in range(len(fov)):
            f.write("circle({}d,{}d,{}d)\n".format(ra[i], dec[i], float(fov[i])/2.))



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
    ps.add_argument("-f", "--footprint", action="store_true", 
                    help="Switch to create a DS9 region file showing the "
                         "footprint of each observation.")
    ps.add_argument("-C", "--color", "--colour", dest="color", default="green",
                    help="Color for the footprint region file.")


    args = ps.parse_args()
    table = open_xml(args.table)

    for source in args.source:
        for chan in args.chan:

            if args.outname is None:
                outname = "{}_{}.txt".format(source, chan)
            else:
                outname = args.outname

            obsids, fov, ra, dec = get_obs(table=table,
                                   source=source,
                                   chan=chan)

            with open(outname, "w+") as f:
                for obs in obsids:
                    f.write("{}\n".format(obs))

            if args.footprint:
                r_outname = outname.replace(".txt", ".reg")
                region_formatter(r_outname, fov, ra, dec, args.color)


if __name__ == "__main__":
    main()
