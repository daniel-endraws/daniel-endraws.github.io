'''
This script parses the contents of input markdown files, extracting links to 
static files, copying them to the output directory. This ensures that unreleased
static files do not exist in the published site but necessary static files are
in the directory before building.
This script is needed since jekyll copies anything in the working directory to
the _site directory, including unreleased static files.

Usage:
python copy.py -i <input markdown file> -f <files directory> -o <output directory>
Example:
python copy.py -i index.md -f ../secret_files -o files

TODO: If we have multiple pages, take in a dir to search for markdown files.
TODO: Depending on how we want to reference static files, we may need to change
the way we parse links.
'''
import re
from pathlib import Path
import shutil
import argparse

def get_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('-i', '--input', type=str, required=True)
  parser.add_argument('-f', '--files', type=str, required=True)
  parser.add_argument('-o', '--output', type=str, required=True)
  return parser.parse_args()

def main():
  args = get_args()
  
  files_dir = Path(args.files)
  output_dir = Path(args.output)
  output_dir.mkdir(parents=True, exist_ok=True)
  
  links = re.findall(r'\[.*\]\((.*)\)', open(args.input).read())
  # Filter out links to external sites.
  files = [l for l in links if not l.startswith('http')]
  
  for f in files:
    f = Path(f)
    # files/homeworks/1/1.pdf -> homeworks/1/1.pdf
    f = Path(*f.parts[1:])
    src = files_dir / f
    dst = output_dir / f
    
    if src.exists():
      dst.parent.mkdir(parents=True, exist_ok=True)
      shutil.copy(src, dst)
    else:
      print('File not found: ', src)
  
if __name__ == '__main__':
  main()