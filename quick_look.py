#! /usr/bin/env python

import numpy as np

from argparse import ArgumentParser
from astropy.io import fits

import matplotlib
import matplotlib.pyplot as plt


def main():

    ps = ArgumentParser(description="Get a quick look at a simple FITS image. "
                                    " This is NOT in world coordinates.")
    ps.add_argument("image")
    ps.add_argument("-m", "--vmin", type=float, default=-0.1)
    ps.add_argument("-M", "--vmax", type=float, default=1.)
    ps.add_argument("-c", "--cmap", type=str, default="viridis")
    ps.add_argument("-s", "--show", action="store_true")
    ps.add_argument("-i", "--inset", action="store_true")

    args = ps.parse_args()
    if not args.show:
        matplotlib.use("Agg")

    if not args.image.endswith(".fits"):
        args.image += ".fits" 

    data = np.squeeze(fits.getdata(args.image))


    fig = plt.figure(figsize=(10, 10))
    ax1 = plt.axes([0, 0, 1, 1])
    ax1.imshow(data, vmin=args.vmin, vmax=args.vmax, cmap=args.cmap)
    ax1.set_xlabel("")
    ax1.set_ylabel("")
    ax1.set_xticks([])
    ax1.set_yticks([])

    if args.inset:

        # Plots a small inset of around the brightest part of image.
        indices = np.where(data == np.nanmax(data))
        i, j = indices[0][0], indices[1][0]
        irange = range(int(max(0, i-0.01*data.shape[-2])),
                       int(min(i+0.01*data.shape[-2], data.shape[-2])))
        jrange = range(int(max(0, j-0.01*data.shape[-1])),
                       int(min(j+0.01*data.shape[-1], data.shape[-1])))

        
        ax2 = plt.axes([0.01, 0.01, 0.2, 0.2])
        
        ax2.imshow(data[int(irange[0]):int(irange[-1])-1, int(jrange[0]):int(jrange[-1])-1], 
                   vmin=args.vmin, vmax=args.vmax, cmap=args.cmap)
       
        ax2.set_xlabel("")
        ax2.set_ylabel("")
        ax2.set_xticks([])
        ax2.set_yticks([])
        
    ax1.text(0.01, 0.99, args.image, 
             horizontalalignment="left",
             verticalalignment="top", 
             transform=ax1.transAxes,
             color="white", 
             fontsize=20.)

    if args.show:
        plt.show()

    fig.savefig(args.image.replace(".fits", "_qa.png"), dpi=300, bbox_inches="tight")


if __name__ == "__main__":
    main()
