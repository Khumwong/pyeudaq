"""
PyEUDAQ - Python bindings for EUDAQ2
"""
import os
import sys
import ctypes

__version__ = "2.0.0"

# Get package directory
_pkg_dir = os.path.dirname(os.path.abspath(__file__))
_lib_dir = os.path.join(_pkg_dir, 'lib')
_so_path = os.path.join(_pkg_dir, 'pyeudaq.so')

# CRITICAL: Pre-load ALL dependencies with RTLD_GLOBAL before loading pyeudaq.so
if os.path.exists(_lib_dir):
    # Load in correct order - core first, then modules
    lib_order = [
        'libeudaq_core.so.2.6',
        'libeudaq_core.so',
    ]
    
    # First, load explicitly ordered libs
    for lib_file in lib_order:
        lib_path = os.path.join(_lib_dir, lib_file)
        if os.path.exists(lib_path):
            try:
                ctypes.CDLL(lib_path, mode=ctypes.RTLD_GLOBAL)
            except Exception as e:
                pass  # May be symlink or already loaded
    
    # Then load any other .so files
    for lib_file in sorted(os.listdir(_lib_dir)):
        if '.so' in lib_file and lib_file not in lib_order:
            lib_path = os.path.join(_lib_dir, lib_file)
            try:
                ctypes.CDLL(lib_path, mode=ctypes.RTLD_GLOBAL)
            except:
                pass

if not os.path.exists(_so_path):
    raise ImportError(f"Compiled library not found: {_so_path}")

# Now that dependencies are loaded, import the native module
import importlib.util
import importlib.machinery

loader = importlib.machinery.ExtensionFileLoader('pyeudaq', _so_path)
spec = importlib.util.spec_from_loader('pyeudaq', loader)
_native = importlib.util.module_from_spec(spec)
sys.modules['_pyeudaq_internal'] = _native

try:
    spec.loader.exec_module(_native)
    
    # Copy all attributes from _native to this module
    _this = sys.modules[__name__]
    for _attr in dir(_native):
        if not _attr.startswith('_'):
            setattr(_this, _attr, getattr(_native, _attr))
    
except Exception as e:
    raise ImportError(f"Failed to load PyEUDAQ native module: {e}")

# Define exports
__all__ = ['__version__'] + [name for name in dir(_native) if not name.startswith('_')]

# Cleanup
del os, sys, ctypes, importlib
del _pkg_dir, _lib_dir, _so_path, loader, spec, _native, _this, _attr
