# Developer's guide

This document explains certain aspects of the development processes. This may be useful if you intend to develop Perylune itself
or want to understand the processes better. The probably only person to ever get interested in this is the author.

# Perylune maintenance

## Managing dependencies

The dependencies required are stored in requirements.in and then compiled into requirements.txt.

```python
pip-compile requirements.in
```


