# Running jupyter

Jupyter notebooks are very convenient way to showcase mix of python
and the graphical results. They're stored in jupyter/ directory.
You can view them by doing the following:

```bash
python -m venv venv
source venv/bin/activate

pip install wheel
pip install poliastro

pip install jupyterlab

pip install tle-tools

jupyterlab
```

And then opening up .jpynb from the jupyter/ directory.
