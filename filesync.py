#!/usr/bin/env python3

import os
import argparse
import shutil
import fnmatch


def synchronize_directories(source_dir, dest_dir, include_patterns=None, exclude_patterns=None):
    for root, dirs, files in os.walk(source_dir):
        for filename in files:
            source_path = os.path.join(root, filename)
            relative_path = os.path.relpath(source_path, source_dir)
            dest_path = os.path.join(dest_dir, relative_path)

            if include_patterns:
                matched_include = any(fnmatch.fnmatch(filename, pattern) for pattern in include_patterns)
                if not matched_include:
                    continue

            if exclude_patterns:
                matched_exclude = any(fnmatch.fnmatch(filename, pattern) for pattern in exclude_patterns)
                if matched_exclude:
                    continue

            if not os.path.exists(dest_path) or os.path.getmtime(source_path) > os.path.getmtime(dest_path):
                shutil.copy2(source_path, dest_path)
                print(f"Copied {source_path} to {dest_path}")


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
