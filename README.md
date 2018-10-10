# mwa_scripts
A collection of scripts for MWA data processing.

#### hms_dms_dd.py
Convert from some string coordinates to decimal degrees. Mostly for easy use in bash scripts. 
```
usage: hms_dms_dd.py RA DEC
```

#### manta.py
Convert list of obersvation IDs to a file suitable to be passed to the manta-ray-client for submitting MWA preprocessing jobs.
```
usage: manta.py OBSLIST -s SELECTION -t TIMERES -f FREQRES -o OUTNAME
```

#### parse_asvo.py
Convert a VOTable (.xml) output from the MWA ASVO, selecting a source and channel (or list of sources and associated channels), outputting single source-channel files listing the observation IDs only. E.g., to be passed to `manta.py`. 
```
usage: parse_asvo.py TABLE -s SOURCE1 SOURCE2 ... -c CHAN1 CHAN2 ... -o OUTNAME
```

#### quick_look.py
Make a quick image in pixel coordinates of a FITS image for a quick look.
```
usage: quick_look.py IMAGE -m VMIN -M VMAX -c COLORMAP
```

#### update_tile_flags.py
Add tile numbers to a file containing a list of observation IDs, for e.g. noting down bad tiles.
```
usage: update_tile_flags.py OBSLIST -t TILE1 TILE2 ... -s SELECTION
```



