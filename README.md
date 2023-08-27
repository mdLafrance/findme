# **findme** [![Pipeline](https://github.com/mdLafrance/findme/actions/workflows/pipeline.yml/badge.svg?branch=main)](https://github.com/mdLafrance/findme/actions/workflows/pipeline.yml) [![Coverage](./reports/coverage/coverage-badge.svg)](./reports/coverage/coverage-badge.svg)
Lightweight python based shell utility for finding files on disk using regex.


## Why?
The bash `find` command has a `--regex` option, which works great for one-off searches.  
However, I didn't have a good way to remember the dozen or so patterns I was searching for daily, and then *quickly* compose them into a `find --regex` call.  

This tool is meant to streamline the process of remembering regex patterns, so you can search for them faster.


## Installation
Use pip to install the `find-patterns` python package: `pip install find-patterns`

This will install a shell script `findme` as well as the python package `find_patterns`.

## Usage
Add a pattern to locate all python files on disk.  
`findme --add py --pattern "\.py$"`             

Add a pattern to locate all c++ template files  
`findme --add templates --pattern "\.(inl|\[ht]cc|\[ht]pp)$"` 
  
Add a pattern to locate all files named "activate". `--files-only` is needed, since the file has no extension to match against.  
`findme --add activate --pattern "activate$" --files-only `  
  
Search for all c++ template files inside the given directory.  
`findme templates ./project_dir/include`
  
Search for maya files and perform other operations with the filepaths.  
`findme maya | wc -l | ...`                                  
  
Remove the alias we previously created for python files.  
`findme --remove py`                                         
  
List all aliases that are assigned.  
`findme --list`                                             
