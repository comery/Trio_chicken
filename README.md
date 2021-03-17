# trio_chicken
scripts for paper "xxx"

```
ref=data/nanopore.asm.fa
asm=data/hifi.asm.fa
p="chicken"
mummer='your-path/mummer4/bin'
$mummer/nucmer --maxmatch -l 100 -c 500 -p $p $ref $asm
$mummer/delta-filter -m -i 90 -l 100 $p.delta > $p.delta.filt
$mummer/dnadiff -d $p.delta -p $p.diff


python3 bin/split_by_chr.py chicken.diff.1coords outdir
cp circos.conf outdir

# do not filter
cd outdir
ls |while read a
do
	cd $a
	awk '{print $12"\t"$1"\t"$2"\t"$13"\t"$3"\t"$4}' $a.links >$a.link.tab
	python3 ../../../bin/preCircosLink.sort.py --scaf_len ../../../data/all.lens --link $a.link.tab
	circos -conf ../circos.conf
	cd ..
done

# filter by scaffold length
awk '$7>98 && $8>=500000 && $9>=500000' chicken.diff.1coords > chicken.diff.1coords.98.500k
python3 ../bin/split_by_chr.py chicken.diff.1coords.98.500k outdir1
cd outdir1
cat list|while read a
do
	cd $a
	awk '{print $12"\t"$1"\t"$2"\t"$13"\t"$3"\t"$4}' $a.links >$a.link.tab
	python3 ../../../bin/preCircosLink.sort.py --scaf_len ../../../data/all.lens --link $a.link.tab
	circos -conf ../circos.conf
	cd ..
done

# filter by align rate
python3 ../bin/filterAlignRate_step.py chicken.diff.1coords.98.500k 0.6 > chicken.diff.1coords.98.500k.0.6
python3 ../bin/split_by_chr.py chicken.diff.1coords.98.500k.0.6 outdir2
cd outdir2
cp ../ourdir/list ./
cp ../outdir/circos ./
cat list|while read a
do
	cd $a
	awk '{print $12"\t"$1"\t"$2"\t"$13"\t"$3"\t"$4}' $a.links >$a.links.tab
	python3 ../../../bin/preCircosLink.sort.py --scaf_len ../../../data/all.lens --link $a.links.tab
	circos -conf ../circos.conf
	cd ..
done

# replace nanopore sequence by hifi sequence
# v1
python3 ../bin/replaceBlock1.py chicken.diff.1coords.98.500k.0.6 ../0.assembly/nanopore.asm.fa ../data/hifi.asm.fa >replaced.fa
# v2
python3 ../bin/MergeLink2Block.py chicken.diff.1coords.98.500k.0.6 >chicken.diff.1coords.98.500k.0.6.bigblock
# manually check chicken.diff.1coords.98.500k.0.6.bigblock, output is synteny.txt
python3 ../bin/replaceBlock_v2.py synteny.txt ../0.assembly/nanopore.asm.fa ../0.assembly/hifi.asm.fa >replaced.v2.fa
```
