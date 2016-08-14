import pdb 
pdb.set_trace()

curr = 0
f = open('phased_convert.vcf','w')
for line in open("/scail/u/xzhou15/CancerProj_10X/whatshap_results/phased.vcf", 'r'):
	print curr
	curr = curr +1
	
	if line[0:2] == '##':
		f.writelines(line) 
	elif line[0:2] == '#C':
		f.writelines(line) 
	
	elif line[0] != '#':
		l = line.rstrip().split('\t')
		try:
                	l[8].index('HP') 			
			s = '\t'.join(l[:9])+'\t' 
			f.writelines(s) 
			
		        for jj in range(9,len(l)):
				if l[jj].split(':')[2] == '.':
					GT = l[jj] + '\t'
					f.writelines(GT) 
				else:
					GT  = str(int(l[jj].split(':')[2].split(',')[0].split('-')[1]) - 1) + '|' + str(int(l[jj].split(':')[2].split(',')[1].split('-')[1]) - 1)  + ':'+ l[jj].split(':')[1] + ':'+ l[jj].split(':')[2] + '\t'
						
					f.writelines(GT) 
			f.writelines('\n') 
													 
		except:
			s = '\t'.join(l[:9])+'\t' 
			f.writelines(s) 
			for jj in range(9,len(l)):
				if l[jj].split(':')[0] == '.':
					GT = l[jj] + '\t'
					f.writelines(GT) 
				else:
					if l[jj].split(':')[0][1] == '|':
						GT = l[jj].split(':')[0][0] + '/' + l[jj].split(':')[0][2] + ':'+ l[jj].split(':')[1] + '\t'
						f.writelines(GT) 
					else:
						GT = l[jj] + '\t'
						f.writelines(GT) 

			f.writelines('\n') 
				            
		
f.close()
