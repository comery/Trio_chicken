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

def main():
    rate_threshold = float(sys.argv[2])
    for rid, blocks in read_ref_block(sys.argv[1]):
        non_overlap_block = []
        que_aligned_region = {}
        short_blocks = []
        for b in blocks:
            b1 = [b[-2], int(b[0]), int(b[1]), b[-1], int(b[2]), int(b[3])]
            short_blocks.append(b1)
            que_seq_len = int(b[8])
            # record the querry information
            if b1[3] in que_aligned_region.keys():
                que_aligned_region[b1[3]] = update_set(que_aligned_region[b1[3]], b1[4], b1[5])
            else:
                que_aligned_region[b1[3]] = init_set(b1[4], b1[5])

            #print(len(list(que_aligned_region[b1[3]])))

        for syn in short_blocks:
            qid, qs, qe = syn[3:]
            qid_aligned_total_base = len(list(que_aligned_region[qid]))
            align_rate = qid_aligned_total_base / que_seq_len
            print("{:.4f}".format(align_rate))
            if align_rate > rate_threshold:
                out = [ str(n) for n in syn]
                print("\t".join(out))



if __name__ == '__main__':
    main()
