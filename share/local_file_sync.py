#!/usr/bin/env python3

import os
import argparse
import shutil
import fnmatch





def main():
    parser = argparse.ArgumentParser(description="Synchronize source directory to destination directory.")
    parser.add_argument("--source", required=True, help="Source directory path")
    parser.add_argument("--dest", required=True, help="Destination directory path")
    parser.add_argument("--include", nargs="+", help="Regex patterns to include files")
    parser.add_argument("--exclude", nargs="+", help="Regex patterns to exclude files")
    args = parser.parse_args()

    source_dir = args.source
    dest_dir = args.dest
    include_patterns = args.include
    exclude_patterns = args.exclude

    synchronize_directories(source_dir, dest_dir, include_patterns, exclude_patterns)


if __name__ == "__main__":
    main()
