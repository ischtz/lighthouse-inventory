# lighthouse-inventory

Ever wonder how many SteamVR devices you actually own? 🤔

This is a simple tool to inventorize all devices that a given SteamVR installation has seen over time. This can be useful for e.g. research labs or VR developers to keep track of their hardware and serial numbers. 

When run without extra arguments, the script will try to guess your SteamVR config directory and generate a list of all previously seen lighthouse receivers (headsets, controllers, trackers). Alternatively, a folder or set of .json files extracted using Valve's lighthouse_console tool can be specified with the ```-j``` argument and is converted to a list in the same way. 

## Command Line Usage 

```
usage: lh_inventory.py [-h] [-j JSON_FILES] [-o output_file] [-u] [-d]

Tool to create a list (CSV) of all tracked Lighthouse devices (e.g. HMD,
controllers, Vive Trackers) known to SteamVR. Alternatively, compiles such a
list from JSON config files downloaded from SteamVR devices using
lighthouse_console.exe.

optional arguments:
  -h, --help            show this help message and exit
  -j JSON_FILES, --json_files JSON_FILES
                        JSON files or folders to convert, e.g. "folder/*.json"
  -o output_file        Ouput file (default: steamvr_inventory.tsv)
  -u                    Update output file instead of overwriting
  -d                    If set, print out JSON and MAT file structures
```

## Building an .exe using PyInstaller

To easily run this on a computer without a full Python install, I've found it helpful to generate a self-contained .exe using PyInstaller by running: 

```
pyinstaller -F lh_inventory.py
```

This will generate an executable in the dist/ subdirectory that should run on any Windows machine. 
