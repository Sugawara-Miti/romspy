# coding: utf-8

import itertools
import shutil

def runs(infile, params):
    
    names = params.keys()
    values = params.values()

    if len(params) == 2:
        case = 0
        for p in itertools.product(values[0], values[1]):
            _paramrep(infile, names, p)
            case += 1
            dirname = 'runs/case{}'.format(case)
            os.mkdir(dirname)
            shutil.copy('oceanM is4dvar.in da_ocean_0b500.10.in',dirname)
            os.chdir(dirname)
            os.system('mpiexec -genv I_MPI_DEVICE rdma -n 16 ./oceanM da_ocean_0b500.10.in > da_log')
            
def _paramrep(infile, paramnames, paramvalues):
    
    with open(infile, 'r') as f:
        context = f.read()

    for name, value in zip(paramnames, paramvalues):
        context = context.replace('$'+name, str(value))

    with open(infile, 'w') as f:
        f.write(context)

if __name__ == '__main__':

    infile = 'da_ocean.tmp'
    params = {'ad_AKT_fac': [1.0e10, 1.0e6],
              'ad_VISC4': [2.0e10, 2.0e5]
              }
    runs(infile, params)
