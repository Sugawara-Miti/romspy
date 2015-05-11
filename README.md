# romspy

Tools for ROMS in Python

### Install
```sh
python setup.py install
```

### example
```py
import romspy

romspy.hview('test.nc', 'test.png', 'temp', t=0, k=20)
```

### future version
```py
import romspy

nc = romspy.dataset(grd='test_grd.nc')
nc.basemap()
```
