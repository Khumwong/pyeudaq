from setuptools import setup, find_packages
import shutil
import os
import platform

system = platform.system()
machine = platform.machine()

print(f"Building for: {system} {machine}")

if system == 'Linux' and machine == 'x86_64':
    # Copy main library - keep original name!
    lib_source = '/home/sutpct/eudaq2/lib/pyeudaq.so'
    lib_dest = 'pyeudaq/pyeudaq.so'  # Don't rename!
    
    os.makedirs('pyeudaq', exist_ok=True)
    os.makedirs('pyeudaq/lib', exist_ok=True)
    
    if os.path.exists(lib_source):
        shutil.copy(lib_source, lib_dest)
        print(f"✓ Copied {lib_source}")
    else:
        raise FileNotFoundError(f"Library not found: {lib_source}")
    
    # Copy dependencies
    eudaq_lib_dir = '/home/sutpct/eudaq2/lib'
    
    # Copy all libeudaq*.so* files
    for file in os.listdir(eudaq_lib_dir):
        if file.startswith('libeudaq') and ('.so' in file):
            src = os.path.join(eudaq_lib_dir, file)
            if os.path.isfile(src):  # Skip symlinks for now
                shutil.copy(src, f'pyeudaq/lib/{file}')
                print(f"✓ Copied {file}")
else:
    print(f"Warning: Building on {system}/{machine}")

setup(
    packages=find_packages(),
    package_data={
        'pyeudaq': ['*.so', '*.pyd', '*.dylib', 'lib/*.so*'],
    },
    include_package_data=True,
)
