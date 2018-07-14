# A scripts to convert a list of observation IDs to a format suitable
# to submit to the MWA manta-ray client, mwa_client, for converting
# snapshots to MeasurementSet format.
# ---------------------------------------------------------------------------- #


def main(obsid_list, selection, timeres, freqres, outname):
    """Prepare manta-ray file.

    e.g.
    obs_id=1151161304, job_type=c, timeres=10, freqres=80, edgewidth=80, \
    	conversion=ms, allowmissing=true, flagdcchannels=true
    """


    with open(obsid_list, "r") as f1:
        obslines = f1.readlines()
        with open(outname, "w+") as f2:
            for i, line in enumerate(obslines):
                if i+1 in selection:
                    
                    obs = line.split()[0]

                    f2.write(line_formatter(obs, timeres, freqres))




def line_formatter(obsid, timeres, freqres, ending="\n"):
    """Create line for manta-ray file."""

    line = "obs_id={0}, job_type=c, timeres={1}, freqres={2}, edgewidth=80, " \
           "conversion=ms, allowmissing=true, flagdcchannels=true{3}".format(
           obsid, timeres, int(freqres), ending)

    return line




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




if __name__ == "__main__":

    import argparse
    ps = argparse.ArgumentParser(description="Convert a list of observation IDs"
                                             " to a manta-ray-client compatible" 
                                             " csv file with appropriate options")

    ps.add_argument("obslist", type=str, help="List of observation IDs.")
    ps.add_argument("-s", "--selection", type=str, help="Which OBS IDs to add.", 
                    default="all")
    ps.add_argument("-t", "--timeres", type=float, help="Time resolution. [4 s]",
                    default=4.)
    ps.add_argument("-f", "--freqres", type=float, help="Frequency resolution. "
                    "[40 kHz]", default=40.)
    ps.add_argument("-o", "--output", "--outname", dest="outname", help="Output"
                    " file name. [`obslist`_manta.csv]", default=None)


    args = ps.parse_args()

    if args.outname is None:
        outname = arg.obslist.split(".")[0]+"_manta.csv"
    else:
        outname = args.outname

    if args.selection == "all":
        selection = "all"
    else:
        selection = convert_selection(args.selection)


    main(args.obslist, selection, args.timeres, args.freqres, outname)









