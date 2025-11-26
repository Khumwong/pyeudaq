# PyEUDAQ

Python bindings for the EUDAQ2 data acquisition framework.

## Features

- Read EUDAQ native format (.raw files)
- Convert events to StandardEvent format
- Access detector plane data
- Extract pixel hit coordinates
- Compatible with ROOT data analysis

## Installation
```bash
pip install pyeudaq
```

**Note:** Currently only supports Linux x86_64. For other platforms, you need to compile EUDAQ2 with Python bindings from source.

## Quick Start
```python
import pyeudaq

# Open a raw data file
reader = pyeudaq.FileReader("native", "run246181002.raw")

# Read events
event_count = 0
while True:
    ev = reader.GetNextEvent()
    if not ev:
        break
    
    print(f"Event {ev.GetEventN()}, Run {ev.GetRunN()}")
    
    # Convert to StandardEvent
    stdev = pyeudaq.StandardEvent()
    pyeudaq.StdEventConverter.Convert(ev, stdev, None)
    
    # Access plane data
    for plane_idx in range(stdev.NumPlanes()):
        plane = stdev.GetPlane(plane_idx)
        nhits = plane.HitPixels()
        print(f"  Plane {plane_idx}: {nhits} hits")
    
    event_count += 1
    if event_count >= 10:
        break
```

## Full Example: Extract Hit Data
```python
import pyeudaq
import numpy as np

reader = pyeudaq.FileReader("native", "data.raw")

all_hits = []

while True:
    ev = reader.GetNextEvent()
    if not ev:
        break
    
    stdev = pyeudaq.StandardEvent()
    pyeudaq.StdEventConverter.Convert(ev, stdev, None)
    
    event_id = ev.GetEventN()
    
    for plane_idx in range(stdev.NumPlanes()):
        plane = stdev.GetPlane(plane_idx)
        plane_id = plane.ID()
        
        for hit_idx in range(plane.HitPixels()):
            x = plane.GetX(hit_idx)
            y = plane.GetY(hit_idx)
            all_hits.append({
                'event_id': event_id,
                'plane_id': plane_id,
                'x': x,
                'y': y
            })

print(f"Extracted {len(all_hits)} total hits")
```

## Requirements

- Python >= 3.6
- NumPy >= 1.19.0
- Linux x86_64 (other platforms require compilation)

## About EUDAQ

EUDAQ is a generic data acquisition framework for common test beam instrumentation, 
developed for the EUDET JRA1 telescope. It provides a flexible and modular system 
for reading out various detectors.

More information: https://eudaq.github.io/

## License

EUPL-1.1 (European Union Public License)

## Support

- Issues: https://github.com/eudaq/eudaq/issues
- Documentation: https://eudaq.github.io/
