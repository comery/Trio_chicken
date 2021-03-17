#!/usr/bin/perl -w
use strict;

if (@ARGV < 2) {
	print "Usage: perl $0 <tab|chr pos1 pos2> <which column>";
	exit()
}
open IN, shift;
my $column = shift;

my %bed;
while (<IN>) {
	chomp;
	my @b = split /\t/;
	my $chr = $b[0];
	my $pos = $b[$column-1];
	$bed{$chr}{$pos} = join("\t", @b);
}

# sort by chr and pos
my @sorted_chrs = sort{$a cmp $b} keys %bed;
for my $chr(@sorted_chrs) {
	my $hash2 = $bed{$chr};
	my @sorted_pos = sort{$a<=>$b} keys %$hash2;
	for my $pos(@sorted_pos){
		print "$bed{$chr}{$pos}\n";
	}
}
close IN;
