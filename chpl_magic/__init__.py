__version__ = '0.0.1'

from .chpl_magic import ChplMagic

def load_ipython_extension(ip):
    ip.register_magics(ChplMagic)
