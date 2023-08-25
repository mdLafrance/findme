# findme [![Pipeline](https://github.com/mdLafrance/findme/actions/workflows/pipeline.yml/badge.svg?branch=main)](https://github.com/mdLafrance/findme/actions/workflows/pipeline.yml) [![Coverage](./reports/coverage/coverage-badge.svg)](./reports/coverage/coverage-badge.svg)
Lightweight python based shell utility for finding files on disk using regex.


## Why?
I found myself having to comb through a filesystem, looking for very specific types of files constantly.  
It was easy enough to use a good old `find . -regex ...` command, but as the list of these types of files grew, abstracting the pattern management away saved a lot of time.

## Installation
Use pip to install the python package: `pip install findme`

This will install a shell script `findme` as well as the python package of the same name.

### Usage
Add a pattern to locate all python files on disk.  
`findme --add py --pattern "\.py$"`             
  
Add a pattern to locate all autodesk maya files (.ma, .mb)  
`findme --add maya --pattern "\.m\[ab]$"`  
  
Add a pattern to locate all c++ template files  
`findme --add templates --pattern "\.(inl|\[ht]cc|\[ht]pp)$"` 
  
Add a pattern to locate all files named "activate"  
`findme --add activate --pattern "activate$" --files-only `  
  
Search for all c++ template files inside the given directory.  
`findme templates ./project_dir/include`
  
Search for maya files and perform other operations with the filepaths.  
`findme maya | wc -l | ...`                                  
  
Remove the alias we previously created for python files.  
`findme --remove py`                                         
  
List all aliases that are assigned.  
`findme --list`                                             
