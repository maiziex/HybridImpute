import matplotlib.pyplot as plt
import numpy as np
import pickle
import pdb
pdb.set_trace()



def process_GT(vcf_file):
	curr = 0
	snp_GT = {}
	for line in open(vcf_file, 'r'):
		print curr 
		curr = curr + 1	
		if line[0]!='#':
			data = line.split('\t')	
			if len(data[3]) ==1 and len(data[4].split(',')[0]) ==1:
				try:
					chr_num = int(data[0])
					chr_name = 'chr' + data[0]
				except:
					chr_name = data[0]
				locus = data[1]
				check_num = chr_name[3:]
				if check_num.isdigit():
					try:
						if data[9].split(':')[0][1] == '/':
        						gt1 = int(data[9].split(':')[0].split('/')[0])
							gt2 = int(data[9].split(':')[0].split('/')[1])
						elif data[9].split(':')[0][1]  == '|':
							gt1 = int(data[9].split(':')[0].split('|')[0])
							gt2 = int(data[9].split(':')[0].split('|')[1])
					except:
						print data[9].split(':')[0]
						gt1 = 0
						gt2 = 0	
			
			
					if snp_GT.has_key(chr_name + ','+ locus):
						snp_GT[chr_name + ','+ locus].append(gt1+gt2)
					else:
						snp_GT[chr_name + ','+ locus] = gt1+gt2


	return snp_GT


#snp_GT1 = process_GT("Files/test.vcf")
#snp_GT2 = process_GT("Files/test2.vcf")
snp_GT1 = process_GT("/home/xzhou15/10X/CEU3/NA12878_GRCh37.vcf")
snp_GT2 = process_GT("/home/xzhou15/10X/NA12878_GIAB_highconf_IllFB-IllGATKHC-CG-Ion-Solid_ALLCHROM_v3.2.2_highconf.vcf")


count  = 0
for key,value in snp_GT1.iteritems():
	if value > 0 :
		count = count +1
	else:
		print key, value

print count

count2= 0
for key,value in snp_GT2.iteritems():
	if value > 0 :
		count2 = count2 +1
	
print count2

overlap = {}
keys_a = set(snp_GT1.keys())
keys_b = set(snp_GT2.keys())
intersection = keys_a & keys_b

intersection2 = []
for idx in intersection:
	if snp_GT1[idx] > 0:
		intersection2.append(idx)


curr = 0
wrong1 = []
wrong2 = []
for idx in intersection2:
	print curr
	curr = curr + 1
	if snp_GT1[idx] == snp_GT2[idx]:
		if overlap.has_key(idx):
			overlap[idx].append(snp_GT1[idx] )
		else:
			overlap[idx]= [snp_GT1[idx]]
	else:
		wrong1.append(snp_GT1[idx])
		wrong2.append(snp_GT2[idx])
		

print "------- Results Report ----------"
print "total snp truth sites:"
print count2
print "total snp called sites:"
print count
print "total snp overlap sites:"
print len(intersection2)
print "total snp overlap and GT correct sites:"
print len(overlap)
print "------------ End ----------------"









				
		
