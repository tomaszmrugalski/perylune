# Obsolete stuff

These are early days experiments. Probably useless now. Kept for historic reasons.

## Running GUI

```python calc-gui.py```

## tools/obstacles-edit

This simple script edits obstacles file for Trimble planning.

Each run can add or delete one obstacle. It can be used several times to edit
a file multiple time. The script is written in python. Each execution requires
two parameters:

- filename
- obstacle definition in format (minazimuth-maxazimuth, angle)

minazimuth and maxazimuth define beginning and ending azimuth, expressed in degrees
angle defines height of an obstacle, also in degrees.

Examples:

If you have a 20 degrees wide obstacle on your East direction that is 45 degrees high, you
can define it with:

```
python obstacle-edit.py obs.txt 80-100,45
```

If you want to define obstacles 160-250 deg, E=60, 300-355 deg, E=70; 45-50 dec, E=55 with:

```
python obstacles-edit.py obs.txt 160-250,60
python obstacles-edit.py obs.txt 300-355,70
python obstacles-edit.py obs.txt 45-50,55
```

## calc-gui.py

A graphical frontend to the Perylune library. It doesn't let you do
much. It's a proof of concept that the library can be used easily in
graphical enviornment as desktop app.

## gps-lab2.py

A script that loads a very simple almanach of 10 GPS satellites with
ECEF coordinates, then calculates azimuth and topocentric height for
specified observer site. Finally, caculates expected GPS precision
(DOP parameters: GDOP, PDOP, HDOP, VDOP, TDOP)

## gps-lab2-competition.py

As part of the lab class, we were supposed to find "the best" set of 4
satellites that provide best DOP parameters. The original intention
was to do it with a bit of trial and error, but that doesn't look like
a proper engineering approach. So I wrote this script. It generates
all 4 element subsets out of 10 satelites and calculates DOP
parameters for them. The results prove conclusively that chosen 4
satelites provide the best possible choice.

Usage:

`python3 tools/gps-lab2-competition.py`

## smog.py

Trivial script used while working on a SmogSAT project.

