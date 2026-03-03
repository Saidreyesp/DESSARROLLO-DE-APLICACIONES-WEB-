import importlib,inspect,sys,os
try:
    m = importlib.import_module('models.conexion')
    f = m.__file__
    print('module file:', f)
    with open(f, 'rb') as fh:
        b = fh.read()
    print('bytes length:', len(b))
    nulls = b.count(b'\x00')
    print('null bytes:', nulls)
    src = inspect.getsource(m)
    print('source length:', len(src))
except Exception as e:
    print('ERROR:', repr(e))
    sys.exit(1)
