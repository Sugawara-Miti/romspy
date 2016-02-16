# romspy

Tools for ROMS in Python

### Install
```sh
git clone https://github.com/okadate/romspy.git
cd romspy
python setup.py install
```

### horizontal view plot
```py
import romspy
nc = romspy.hview.Dataset('test_his.nc')

# s-coordinate plot
nc.sview(vname='temp', t=0, k=0)

# z-level plot
nc.zview(vname='temp', t=0, depth=0)
```
