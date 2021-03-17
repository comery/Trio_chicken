#!/usr/bin/env python3
import sys
import os

if len(sys.argv) < 3:
    sys.exit("python3 {} <*.1corrds> <outdir>".format(sys.argv[0]))

def main():
    outdir = sys.argv[2]
    records = {}
    with open(sys.argv[1], 'r') as fh:
        for i in fh:
            tmp = i.strip().split()
            ref_scaf = tmp[0].split("-")[0]
            if ref_scaf in records.keys():
                records[ref_scaf].append(i.strip())
            else:
                records[ref_scaf] = [i.strip(),]

    for k in records.keys():
        sub_outdir = os.path.join(outdir, k)
        outfile = os.path.join(sub_outdir, k + ".links")
        if os.path.exists(sub_outdir) == False:
            os.makedirs(sub_outdir)
        with open(outfile, 'w') as fw:
            fw.write("\n".join(records[k]))


if __name__ == '__main__':
    main()
