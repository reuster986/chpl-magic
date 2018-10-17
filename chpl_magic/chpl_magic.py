import importlib.util
import os
import sys
import time
from subprocess import Popen, PIPE
from glob import glob
try:
    import hashlib
except ImportError:
    import md5 as hashlib
from IPython.core.magic import Magics, magics_class, cell_magic
try:
    from IPython.paths import get_ipython_cache_dir
except ImportError:
    # older IPython version
    from IPython.utils.path import get_ipython_cache_dir

@magics_class
class ChplMagic(Magics):

    def __init__(self, shell):
        super(ChplMagic, self).__init__(shell)
        self._reloads = {}
        self._code_cache = {}

    def _import_all(self, module):
        module.chpl_setup()
        mdict = module.__dict__
        if '__all__' in mdict:
            keys = mdict['__all__']
        else:
            keys = [k for k in mdict if not k.startswith('_')]

        for k in keys:
            try:
                self.shell.push({k: mdict[k]})
            except KeyError:
                msg = "'module' object has no attribute '%s'" % k
                raise AttributeError(msg)
                
    def _load_module(self, modname, basepath):
        globstr = os.path.join(basepath, modname, 'chpl.*.so')
        res = glob(globstr)
        if len(res) == 1:
            spec = importlib.util.spec_from_file_location('chpl', res[0])
        else:
            raise ImportError(f'No unique found: {res}')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self._import_all(module)
        
                
    @cell_magic
    def chpl(self, line, cell):
        code = cell if cell.endswith('\n') else cell+'\n'
        lib_dir = os.path.join(get_ipython_cache_dir(), 'chpl')
        key = (code, line, sys.version_info, sys.executable, time.time())
        if not os.path.exists(lib_dir):
            os.makedirs(lib_dir)
        module_name = "_chpl_magic_" + hashlib.md5(str(key).encode('utf-8')).hexdigest()
        src_path = os.path.join(lib_dir, module_name + '.chpl')
        cmd = ['chpl', 
               '--library', 
               '--library-python',
               f'--library-dir={lib_dir}',
               f'--library-python-name={module_name+".chpl"}']
        cmd.extend(line.split())
        # pyname = os.path.join(tdir.name, 'mycode')
        with open(src_path, 'w') as f:
            f.write(code)
        cmd.append(src_path)
        call = Popen(cmd, stdout=PIPE, stderr=PIPE)
        out, err = call.communicate()
        print(out.decode())
        print(err.decode())
        self._load_module(module_name, lib_dir)
