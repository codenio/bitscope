from distutils.core import setup, Extension

module = Extension ( 'bitlib', libraries = ['BitLib'], sources = ['bitlibmodule.c'] )

setup ( name = "bitlib", version = "2.0", 
        maintainer = "BitScope Designs", maintainer_email = "support@bitscope.com",
        description = "BitScope Library Python Extension module", ext_modules = [module] )
