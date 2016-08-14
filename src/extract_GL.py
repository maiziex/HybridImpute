import matplotlib.pyplot as plt
import numpy as np
import pickle
import pdb
pdb.set_trace()



def process_GL(vcf_file):
	f = open('trio_GL.txt','w')
	curr = 0
	snp_GL = {}
	for line in open(vcf_file, 'r'):
		print curr 
		curr = curr + 1	
		if line[0]!='#':
			data = line.split('\t')	
			if len(data[3]) ==1 and len(data[4].split(',')[0]) ==1:				
			        chr_name = data[0]
		        	locus = data[1]
				try:
                			i_GL = data[8].split(':').index('GL')	
				except:
					continue			
				s_GL_all = ''
                		for i_GT in range(9, len(data)):
                    			s_GL = data[i_GT].split(':')[i_GL]
                    			if s_GL == '.':
                        			break
                    			else:
						s_GL_all = s_GL_all+ s_GL + '\t'
           			if s_GL == '.':
                        		continue
				else:
					f.writelines(s_GL_all + '\n')
						
	return snp_GL


#snp_GL2 = process_GL("Files/test2.vcf")
snp_GL1 = process_GL("Files/test_trio2.vcf")


	
