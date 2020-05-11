# romspy

Tools for ROMS in Python

## Installation

Requiring module

- netCDF4

```sh
git clone https://github.com/okadate/romspy.git
cd romspy
python setup.py install
```

## Example

### Horizontal view plot
```py
import romspy
nc = romspy.hview.Dataset('test_his.nc')

# s-coordinate plot
nc.sview(vname='temp', t=0, k=0)

# z-level plot
nc.zview(vname='temp', t=0, depth=0)
```
