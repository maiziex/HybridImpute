import pdb
pdb.set_trace()
from find_highconf_locus import *
import sys

highconf_locus = find_highconf(sys.argv[1])
fw = open("phased_variants_chr20_addhighconfflag.vcf","w")
#fw = open("10X_trio_chr20_HighCon_SNP_addflag.vcf","w")
#fw = open("10X_trio_chr20_SNP_together_trio_highconf.vcf.recode.vcf","w")
#f = open("/scail/u/zhanglu2/LinkFam/varcall/10X_trio_chr20_SNP_together_trio.vcf.recode.vcf","r")
f = open("phased_variants_chr20.vcf","r")
#f = open(sys.argv[1],"r")
curr  = 0
for line in f:
    print(curr)
    curr += 1
    if line[0:2] == "##":
        fw.writelines(line)
    elif line[0:2] == "#C":
        fw.writelines(line.rstrip()+"\t" + "HighConf"+"\n")

    if line[0]!="#":
        data  = line.rstrip().split("\t")
        curr_locus = data[1]
        data_new = "\t".join(data)+"\t"
        if curr_locus in highconf_locus:
            highconf_flag = 1
        else:
            highconf_flag = 0
        fw.writelines(data_new+str(highconf_flag)+"\n")


print highconf_locus
