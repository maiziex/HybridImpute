import pdb
pdb.set_trace()



def process_GT(vcf_file, sample_idx ):
	curr = 0
	count1 = 0
	count2 = 0


	variant_GT_nophased = []
	variant_GT_phased = {}
	variant_GT_phased2 = {}
	variant_GTcontent_phased = {}

	whatshap_variant_GT_nophased = []
	whatshap_variant_GT_phased = {}
	whatshap_variant_GT_phased2 = {}
	whatshap_variant_GTcontent_phased = {}
	
	for line in open(vcf_file, 'r'):
		print curr 
		curr = curr + 1	
		if line[0]!='#':
			data = line.split('\t')				
			chr_name = data[0]
			locus = data[1]
			try:

				if data[sample_idx].split(':')[0][1] == '/':
        				variant_GT_nophased.append([chr_name , locus])
					
				elif data[sample_idx].split(':')[0][1]  == '|':
					count1 = count1 + 1
					GTcontent_phased = data[sample_idx].split(':')[0]
					blk = data[sample_idx].split(':')[1]
					

					variant_GTcontent_phased[(chr_name, locus)] = GTcontent_phased
					if variant_GT_phased.has_key((chr_name, blk)):
						variant_GT_phased[(chr_name, blk)].append(locus)
					else:
						variant_GT_phased[(chr_name, blk)] = [locus]

					if variant_GT_phased2.has_key((chr_name, locus)):
						variant_GT_phased2[(chr_name, locus)].append(blk)
					else:
						variant_GT_phased2[(chr_name, locus)] = [blk]
					
			except:
				print data[sample_idx]
				

			try:
				whatshap = data[sample_idx].split(':')[2]
				whatshap_blk = whatshap.split(',')[0].split('-')[0]
				whatshap_GTcontent_phased = str(int(whatshap.split(',')[0].split('-')[1])-1) + '|' + str(int(whatshap.split(',')[1].split('-')[1])-1) 
				whatshap_variant_GTcontent_phased[(chr_name, locus)] = whatshap_GTcontent_phased
				count2 = count2 + 1
				if whatshap_variant_GT_phased.has_key((chr_name, whatshap_blk)):
					whatshap_variant_GT_phased[(chr_name, whatshap_blk)].append(locus)
				else:
					whatshap_variant_GT_phased[(chr_name, whatshap_blk)] = [locus]

				if whatshap_variant_GT_phased2.has_key((chr_name, locus)):
					whatshap_variant_GT_phased2[(chr_name, locus)].append(whatshap_blk)
				else:
					whatshap_variant_GT_phased2[(chr_name, locus)] = [whatshap_blk]
			except:
				if data[sample_idx].split(':')[0] == '.':
					print data[sample_idx]
				
				else:
					#print data[sample_idx]
					whatshap_variant_GT_nophased.append([chr_name , locus])
			
			

	return variant_GT_nophased, variant_GT_phased,variant_GT_phased2, variant_GTcontent_phased, whatshap_variant_GT_nophased, whatshap_variant_GT_phased,whatshap_variant_GT_phased2, whatshap_variant_GTcontent_phased



#(variant_GT_nophased, variant_GT_phased,variant_GT_phased2, variant_GTcontent_phased, whatshap_variant_GT_nophased, whatshap_variant_GT_phased,whatshap_variant_GT_phased2, whatshap_variant_GTcontent_phased) = process_GT("/Users/maiziex/10X/Files/test_phased.vcf", sample_idx = 9)
(variant_GT_nophased, variant_GT_phased,variant_GT_phased2, variant_GTcontent_phased, whatshap_variant_GT_nophased, whatshap_variant_GT_phased,whatshap_variant_GT_phased2, whatshap_variant_GTcontent_phased) = process_GT("/scail/u/xzhou15/CancerProj_10X/whatshap_results/phased.vcf", sample_idx = 9 )




keys_a = set(whatshap_variant_GTcontent_phased.keys())
keys_b = set(variant_GTcontent_phased.keys())

intersection = keys_a & keys_b

count3 = 0
count4 = 0
count5 = 0
count6 = 0
line  = 0
for chrloc in intersection:
	print line
	line = line +1
	chr_name  = chrloc[0]	
	locus =  chrloc[1]	
	whatshap_blk = whatshap_variant_GT_phased2[chrloc][0]
	whatshap_cur_blk_num = whatshap_variant_GT_phased[(chr_name,whatshap_blk)]
	GT_whatshap = whatshap_variant_GTcontent_phased[(chr_name, locus)]	

	blk = variant_GT_phased2[chrloc][0]
	cur_blk_num = variant_GT_phased[(chr_name,blk)]
	GT = variant_GTcontent_phased[(chr_name, locus)]

	whatshap_idx  = whatshap_cur_blk_num.index(locus) 
	idx  = cur_blk_num.index(locus) 

        interset = set(whatshap_cur_blk_num) & set(cur_blk_num)
	
	whatshap_GT_all_1 = []
	whatshap_GT_all_2 = []
	GT_all_1 = []
	GT_all_2 = []
	for pos in interset:
		whatshap_GT_all_1.append(whatshap_variant_GTcontent_phased[(chr_name, pos)].split('|')[0])
		whatshap_GT_all_2.append(whatshap_variant_GTcontent_phased[(chr_name, pos)].split('|')[1])
		GTs_whatshap_1 = ' '.join(whatshap_GT_all_1)
		GTs_whatshap_2 = ' '.join(whatshap_GT_all_2)

		GT_all_1.append(variant_GTcontent_phased[(chr_name, pos)].split('|')[0])
		GT_all_2.append(variant_GTcontent_phased[(chr_name, pos)].split('|')[1])
		GTs_1 = ' '.join(GT_all_1)
		GTs_2 = ' '.join(GT_all_2)
		
		
	if GTs_whatshap_1 == GTs_1 and GTs_whatshap_2 == GTs_2:
		count3 = count3 + 1
	elif GTs_whatshap_1 == GTs_2 and GTs_whatshap_2 == GTs_1:
		count4 = count4 + 1
	else:
		count5 = count5 + 1
		




print len(keys_a), len(keys_b)
print len(intersection), count3,count4,count5








				
		
