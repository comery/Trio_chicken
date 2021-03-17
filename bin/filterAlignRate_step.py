#!/usr/bin/env python3
import sys
if len(sys.argv) < 3:
    sys.exit("python3 {} <*.1coords> <rate cutoff>".format(sys.argv[0]))


def read_ref_block(inputfile):
    pre = ""
    with open(inputfile, 'r') as fh:
        while True:
            line = fh.readline().strip()
            if not line:
                break
            tmp = line.split()
            if pre == "":
                block = [tmp,]
                pre = tmp[-2]
            elif tmp[-2] == pre:
                block.append(tmp)
            else:
                yield tmp[-2], block
                block = [tmp,]
                pre = tmp[-2]

        yield tmp[-2], block


def init_set(start, end):
    set0 = set()
    if end < start:
        start, end = end, start
    for i in range(start, end):
        set0.add(i)
    return set0

def update_set(set0, start, end):
    if end < start:
        start, end = end, start
    for i in range(start,end):
        set0.add(i)
    return set0

def update_region(lens, pre_region, cur_region):
    a, b = pre_region
    c, d = cur_region
    if b < a:
        a, b = b, a
    if d < c:
        c, d = d, c

    cur_len = d - c + 1
    if c >= a and d <= b:
        # covered by previous
        sum_len = lens
        return (a,b), sum_len
    elif c > a and c < b:
        # partial overlap
        overlap_len = b - c + 1
        sum_len = lens + cur_len - overlap_len
        return (c,d), sum_len
    elif d > a and d < b:
        overlap_len = d - a + 1
        sum_len = lens + cur_len - overlap_len
        return (c,d), sum_len
    else:
        # no overlap
        sum_len = lens + cur_len
        return (c,d), sum_len



def main():
    rate_threshold = float(sys.argv[2])
    kept = set()
    for rid, blocks in read_ref_block(sys.argv[1]):
        non_overlap_block = []
        que_aligned_len = {}
        short_blocks = []
        for b in blocks:
            b1 = [b[-2], int(b[0]), int(b[1]), b[-1], int(b[2]), int(b[3])]
            short_blocks.append(b1)
            que_seq_len = int(b[8])
            if b1[4] > b1[5]:
                cur_region = (b1[5], b1[4])
            else:
                cur_region = (b1[4], b1[5])
            # record the querry information
            if b1[3] not in que_aligned_len.keys():
                que_aligned_len[b1[3]] = abs(b1[5] - b1[4]) + 1
                pre_region = cur_region
            else:
                # the valuse is a list[ sum_length, previous_region, current_region ]
                pre_region, que_aligned_len[b1[3]] = update_region(que_aligned_len[b1[3]], pre_region, cur_region)
            #print(que_aligned_len[b1[3]])


        for syn in short_blocks:
            rid, rs, re, qid, qs, qe = syn
            align_rate = que_aligned_len[qid] / que_seq_len
            if align_rate > rate_threshold:
                kept.add((rid,qid))

    with open(sys.argv[1], 'r') as fh:
        for i in fh:
            tmp = i.strip().split()
            if (tmp[-2], tmp[-1]) in kept:
                print(i.strip())


if __name__ == '__main__':
    main()
