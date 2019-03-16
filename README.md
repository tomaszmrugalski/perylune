# astro
Tools related to orbital mechanics and related topics.

## obstacles-edit

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
