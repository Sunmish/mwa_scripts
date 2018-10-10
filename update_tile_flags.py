#! /usr/bin/env python

from argparse import ArgumentParser


def read_obslist(obslist):
    """Read in OBS ID list.

    This may be simply a list of OBS IDs, and optionally a list of 
    tiles to flag per snapshot.
    """

    obs_ids, obs_flags = [], []

    with open(obslist, "r") as obs:

        lines = obs.readlines()
        for line in lines:
            bits = line.replace("\n", "").rstrip().split(" ")
            if len(bits) == 1:  # No flag tiles on this line.
                flags = ""
            elif len(bits) == 2:
                flags = bits[1]
            else:
                raise ValueError("OBS ID file line has too many items: \n" \
                                 "{0}".format(line))

            obs_ids.append(bits[0])
            obs_flags.append(flags)

    return obs_ids, obs_flags


def convert_selection(selection):
    """Convert selection from e.g. 1-5 to [1, 2, 3, 4, 5].

    This selection format is the same Slurm's `array` selection.
    """


    bits = selection.split(",")
    all_bits = []
    for bit in bits:
        small_bits = bit.split("-")
        if len(small_bits) == 1:
            all_bits.append(int(small_bits[0]))
        else:
            range_of_bits = range(int(small_bits[0]), int(small_bits[1])+1)
            for tiny_bit in range_of_bits:
                all_bits.append(tiny_bit)

    return all_bits



def main():
    """The main function."""

    ps = ArgumentParser(description="Add tile numbers to a file listing MWA "
                                    "observation IDs, presumably to note down "
                                    "bad tiles to be flagged.",
                        epilog="Each line in the file should be: OBSID1 1,123,3,..."
                        )

    ps.add_argument("obsid_list", nargs="*", 
                    help="List of observation IDs.")
    ps.add_argument("-t", "--tiles", type=str,
                    help="Tile numbers.")
    ps.add_argument("-s", "--selection", type=str, help="Selection, 1-indexed, "
                    "of observation IDs to add tiles to. E.g., 1-5 or 1,2.")
    ps.add_argument("-r", "--remove", action="store_true", help="Switch to "
                    "remove selected tiles from the present tiles instead of "
                    "adding them. [Default add]")

    args = ps.parse_args()

    if args.tiles is None:
        raise ValueError("Tiles must be specified.")

    if args.selection is not None:
        selection = convert_selection(args.selection)
    else:
        selection = range(1, 1e5)  # Max 10 000-1? Should be reasonable. 
    tiles = [str(t) for t in convert_selection(args.tiles)]
    tiles_str = ""
    for t in tiles:
        tiles_str += "{},".format(t)
    tiles_str = tiles_str[:-1]

    for obs_list in args.obsid_list:
        obs_ids, obs_flags = read_obslist(obs_list)

        with open(obs_list, "w+") as f:
            for i in range(len(obs_ids)):
                if i+1 in selection:

                    if args.remove:
                        new_flags = ""
                        orig_flags = obs_flags[i].split(",")
                        for orig_flag in orig_flags:
                            # print orig_flag
                            if orig_flag not in tiles:
                                new_flags += "{},".format(orig_flag)
                                print new_flags
                        new_flags = new_flags[:-1]
                    else:
                        if obs_flags[i] == "":
                            new_flags = "{}".format(tiles_str)
                        else:
                            new_flags = "{},{}".format(obs_flags[i], tiles_str)

                    f.write("{} {}\n".format(obs_ids[i], new_flags))
                else:
                    f.write("{} {}\n".format(obs_ids[i], obs_flags[i]))


if __name__ == "__main__":
    main()
