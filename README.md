# mwa_scripts
A collection of scripts for MWA data processing.

*`parse_asvo.py`: Convert a VOTable (.xml) output from the MWA ASVO, selecting a source and channel (or list of sources and associated channels), outputting single source-channel files listing the observation IDs only. E.g., to be passed to `manta.py`. 

*`update_tile_flags.py`: Add tile numbers to a file containing a list of observation IDs, for e.g. noting down bad tiles.

*`manta.py`: Convert list of obersvation IDs to a file suitable to be passed to the manta-ray-client for submitting MWA preprocessing jobs.


