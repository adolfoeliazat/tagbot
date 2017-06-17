# tagbot

`tagbot` is a [LEGO Mindstorms NXT](https://en.wikipedia.org/wiki/Lego_Mindstorms_NXT) robot for testing passive integrated transponder (PIT) tags and readers, controlled using python scripts.  `tagbot` was implemented by [Trident Systems](https://www.tridentsystems.co.nz/) for testing tags and readers for use in fish tagging programmes that aim to estimate stock abundance using mark-recapture methods.

Two different robots have been implemented, `approach` and `scan`.

## approach testing

The `approach` testing robot is designed to test tag detection distance with the tag presented to the antenna in different orientations.  The robot carries the tag hotizontally towards a vertically mounted antenna.  This facilites grid testing of detection distance across the surface of the antenna.

## scan testing

The `scan` testing robot carries a tag at different heights across a horisontally mounted antenna.  This is intended to simulate the scanning of a fish over an antenna incorporated in a catch sorting table.

## Requirements

The robot building instructions are given in LXF files.  These can be viewed in LEGO Digital Designer.

The standard Mindstorms distance sensor was replaced with ...

This has been tested using a Biomark IS1001 tag reader.

The Mindstorms robot and the tag reader connect to the host computer using USB cables.

## Installation

On Ubuntu linux flavours, install the `python-nxt` and `python-usb` packages.

Install `python-usb` using your distribution's package manager, then follow the instructions beginning "For USB communications ..." at https://github.com/Eelviny/nxt-python/wiki/Installation to set permissions etc.

## Use

To communicate with the tag reader, the program must be run with elevated permission. i.e. sudo.

The `approach` tagbot expects two command line parameters: a tag ID and a grid position.  Each approach test results in a line output on stdout.

`sudo approach.py <tagID> <gridID>`

The `scan` tagbot expects a single command line parameter: a tag ID.

`sudo scan.py <tagID>`



