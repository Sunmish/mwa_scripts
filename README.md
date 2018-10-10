# mwa_scripts
A collection of scripts for MWA data processing.

*`hms_dms_dd`: Convert from some string coordinates to decimal degrees. Mostly for easy use in bash scripts. 

*`manta.py`: Convert list of obersvation IDs to a file suitable to be passed to the manta-ray-client for submitting MWA preprocessing jobs.

*`parse_asvo.py`: Convert a VOTable (.xml) output from the MWA ASVO, selecting a source and channel (or list of sources and associated channels), outputting single source-channel files listing the observation IDs only. E.g., to be passed to `manta.py`. 

*`quick_look.py`: Make a quick image in pixel coordinates of a FITS image for a quick look.

*`update_tile_flags.py`: Add tile numbers to a file containing a list of observation IDs, for e.g. noting down bad tiles.




