#!/usr/bin/env python3
#Author: Kritika Garg
# Usage: For each domain, we have a predefined target number of URLs (NR) for our final downsampled dataset. This script selects that number of URLs from the file containing the first CDX entries for each URL, prioritizing the root page first and then adding deeper links.
# ~/code/sep_downsampledata.py ~/htmllike/yearwise/domain_dist.old/downsampling10/log_downsampling/cdx_sample_107M.$i.domains.log $i/cdx_sample_107M.html.clean.allrooturls.domain.depth.$i $i/cdx_sample_107M.html.clean.other.domain.depth.$i  $i/cdx_sample_107M.html.clean.allrooturls.domain.depth.$i.downsample $i/cdx_sample_107M.html.clean.other.domain.depth.$i.downsample

import sys

f1 = open(sys.argv[1],'r', errors='ignore')
downsamp_dict = {}

for line in f1:
	line = line.strip('\n')
	domainN, N, NR = line.split('\t')
	count = 0
	downsamp_dict[domainN] = (int(NR),count)
f1.close()

def main_func(fname_inp, root):
	with open(fname_inp,'r', encoding="utf8", errors='ignore') as file:
		for line in file:
			line = line.strip('\n')
			cdx, ext, sub, domain, suffix, depth, path = line.split('\t')
			domainN = domain + "." + suffix
			if domainN in downsamp_dict:
				NR,count = downsamp_dict[domainN]
				if root:
					fwr.write(line+'\n')
				else:
					fwo.write(line+'\n')
				count+=1
				if count == NR:
					print(domainN+"\t"+str(NR)+"\t"+str(count))
					del downsamp_dict[domainN]
				else:
					downsamp_dict[domainN] = (int(NR),count)
			else:
				continue

	file.close()

fwr = open(sys.argv[4],'w')
fwo = open(sys.argv[5],'w')
main_func(sys.argv[2], root=True)
main_func(sys.argv[3], root=False)

