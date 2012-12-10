#!/usr/bin/env python3
import os
import sys
import json

EXTENSIONS = [".scala", ".js", ".py", ".java", ".cs", ".rb"]

def count_lines(filename):
    lines = 0

    for line in open(filename):
        lines += 1

    return lines

def to_d3_format(data, name):
    children = []

    result = {"name": name, "children": children}

    for key in data:
        value = data[key]

        if isinstance(value, dict):
            children.append(to_d3_format(value, key))
        else:
            children.append({"name": key, "size": value})

    return result

def walk(path="."):
    result = {}

    for dirname, dirnames, filenames in os.walk(path):
        accum = result
        for dirpart in dirname.split("/"):
            if dirpart in accum:
                accum = accum[dirpart]
            else:
                accum[dirpart] = {}
                accum = accum[dirpart]

        for filename in filenames:

            if not any(filename.endswith(extension) for extension in EXTENSIONS):
                continue 

            filepath = os.path.join(dirname, filename)
            try:
                accum[filename] = count_lines(filepath)

            except IOError:
                pass

    return result

def main():
    current_path = os.getcwd()
    os.chdir(sys.argv[1])
    result = walk(".")
    d3data = to_d3_format(result, "root")

    print(open(os.path.join(current_path, "treezoom.html")).read())
    print("showJson(", end="")
    print(json.dumps(d3data, indent=2))
    print(");</script></body></html>")

if __name__ == "__main__":
    main()

