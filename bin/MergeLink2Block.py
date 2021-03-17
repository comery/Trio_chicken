#!/usr/bin/env python3
import sys
import os
if len(sys.argv) < 2:
    sys.exit("python3 {} <$a.1coords>".format(sys.argv[0]))


def main():
    link = {}
    lens = {}
    with open(sys.argv[1], 'r') as fh:
        for i in fh:
            tmp = i.strip().split()
            lens[tmp[-2]] = tmp[7]
            lens[tmp[-1]] = tmp[8]
            pair = tmp[-2] + "_" + tmp[-1]
            if pair not in link.keys():
                link[pair] = [tmp[0:4],]
            else:
                link[pair].append(tmp[0:4])


    for x in link.keys():
        ids = x.split("_")
        target_start = link[x][0][0]
        target_end = link[x][-1][1]
        que_start = link[x][0][2]
        que_end = link[x][-1][-1]
        out = [ ids[0], target_start, target_end, ids[1], que_start, que_end, lens[ids[0]], lens[ids[1]] ]
        print("\t".join(out))



if __name__ == '__main__':
    main()
