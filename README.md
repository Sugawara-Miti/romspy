# romspy

Tools for ROMS in Python

## How to install

```sh
cd romspy
python setup.py install
```

## example

```py
import romspy

nc = romspy.dataset(grd='test_grd.nc')
nc.basemap()
```
