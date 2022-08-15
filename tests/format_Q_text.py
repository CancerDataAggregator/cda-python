import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file", type=argparse.FileType("r"))
args = parser.parse_args()

d = args.file.name.replace("./", "").replace(".", "-copy.")
with open(d, "w") as f:
    for i in args.file.readlines():
        f.write(str(i).replace(",", ",\n"))
