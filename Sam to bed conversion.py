# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import sys
# argparse will talk to the command-line and assign anything typed after --samfile to the variable args.samfile which is called allter
#This allows us to automate the sam to bed file conversion in command-line by calling an 
import argparse

parser=argparse.ArgumentParser(description = "Convert sam to bed")

parser.add_argument('--samfile', help='sam file input')
args=parser.parse_args()
parser.add_argument('--bedfile', help='bed file output', default =str(args.samfile).replace(".sam",".bed"))
#alternative solution
#default =(str(args.samfile).rsplit(".",1)[0]+".bed"))
parser.add_argument('-p', help = 'amount to pad', required = False, default=0)


args=parser.parse_args()

if str(args.samfile).rsplit(".",1)[1] !="sam":
    raise Exception ('Are you sure this is a SAM file?')
else:
    pass

samfile = open(args.samfile, 'r')
output = open(args.bedfile, 'w')
for line in samfile:
    if line.startswith('@'):
        continue
    elif 'XS:A:' not in line: 
        continue 
    # miss out lines without a strandedness
    else:
        # split line into strings
       splitline = (line.split('\t'))
       if splitline[2] == '*':
           continue 
       # unmapped reads can't go into the bed file
       else:
           chrom = splitline[2]
           SAMfile_start = (int(splitline[3])-1)
           read_length = len(splitline[9])
           gene_name = (splitline[0])
           thestrand =0
      
           if 'XS:A:-' in line: 
               thestrand = '-'
               stop = SAMfile_start
               # for negative stranded SAMfile_start defines the stop position of read
               start = stop - read_length
               # the start position for negative strands will be before the number in column 4 on SAM file
               
           elif 'XS:A:+' in line:
               thestrand = '+'
               start = SAMfile_start
               # for postive strand start position equivalent to column 4 in SAM file
               stop = start + read_length
               # for positive strand stop postion will be after number contained in column 4 of SAM file
           bed = '%(chrom)s\t%(start)s\t%(stop)s\t%(gene_name)s\t.\t%(thestrand)s\n' %locals()
           #string formatting of bed file
    print(bed)
    output.write(bed)
output.close()


         
    


# command line parameters (SAM file, BED)
# read our file
#iterate over each line
# ignore headers
#split the line up
#assign each flag to a variable
# create missing variables
#order the variable and print them out to a new file (BED)
# order: chr, start, stop, read_name, empty, strd.