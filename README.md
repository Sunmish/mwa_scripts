# mwa_scripts
A collection of scripts for MWA data processing.

*`copyselect.sh`: Move data around on Pawsey (e.g. /group to /astro and vice versa). This assumes you have been using Thomas Franzen's MWA processing pipeline.

*`manta.py`: Convert list of obersvation IDs to a file suitable to be passed to the manta-ray-client for submitting MWA preprocessing jobs.

*`parse_asvo.py`: Convert a VOTable (.xml) output from the MWA ASVO, selecting a source and channel (or list of sources and associated channels), outputting single source-channel files listing the observation IDs only. E.g., to be passed to `manta.py`. 
