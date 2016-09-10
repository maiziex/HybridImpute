from collections import defaultdict
import pdb
pdb.set_trace()


class sample(object):
    def __init__(self,GT_hp1,RO_hp1,AO_hp1,GT_hp2,RO_hp2,AO_hp2):
        self.GT_hp1 = GT_hp1
        self.RO_hp1 = RO_hp1
        self.AO_hp1 = AO_hp1
        self.GT_hp2 = GT_hp2
        self.AO_hp2 = AO_hp2
        self.RO_hp2 = RO_hp2



def main():
    highconf_locus = []
    count = 0
    f = open("/scail/u/zhanglu2/LinkFam/varcall/10X_trio_chr20_HighCon_SNP.vcf","r")
    curr = 0
    reads_depth = 2
    for line in f:
        print curr
        curr += 1
        if line[0]!="#":
            samples = []
            GT_hp1_count = defaultdict()
            GT_hp2_count = defaultdict()
            data = line.rsplit()
            try:
                for field in [9,12,15]:
                    GT_hp1 = data[field].split(":")[0]
                    RO_hp1 = int(data[field].split(":")[3])
                    AO_hp1 = int(data[field].split(":")[5])

                    GT_hp2 = data[field+1].split(":")[0]
                    RO_hp2 = int(data[field+1].split(":")[3])
                    AO_hp2 = int(data[field+1].split(":")[5])
                    
                    new_sample = sample(GT_hp1,RO_hp1,AO_hp1,GT_hp2,RO_hp2,AO_hp2)
                    samples.append(new_sample)
                          
                          
                count += 1
                if (samples[0].GT_hp1=="0/0" or samples[0].GT_hp1=="1/1") and (samples[0].GT_hp2=="0/0" or samples[0].GT_hp2=="1/1") and (samples[1].GT_hp1=="0/0" or samples[1].GT_hp1=="1/1") and (samples[1].GT_hp2=="0/0" or samples[1].GT_hp2=="1/1") and  (samples[2].GT_hp1=="0/0" or samples[2].GT_hp1=="1/1") and (samples[2].GT_hp2=="0/0" or samples[2].GT_hp2=="1/1"):
                    for ii in range(3):
                        if samples[ii].GT_hp1=="0/0":
                            GT_hp1_count[ii] = samples[ii].RO_hp1
                        elif samples[ii].GT_hp1=="1/1":
                            GT_hp1_count[ii] = samples[ii].AO_hp1

                        if samples[ii].GT_hp2=="0/0":
                            GT_hp2_count[ii] = samples[ii].RO_hp2
                        elif samples[ii].GT_hp2=="1/1":
                            GT_hp2_count[ii] = samples[ii].AO_hp2
                        
       

                    if GT_hp1_count[0] >=reads_depth and GT_hp2_count[0]>=reads_depth and GT_hp1_count[1] >=reads_depth and GT_hp2_count[1] >=reads_depth and GT_hp1_count[2] >=reads_depth and GT_hp2_count[2]>=reads_depth:
                        highconf_locus.append(data[1])


            except:
                count += 1
                pass
      

    print count,len(highconf_locus),float(len(highconf_locus))/count


if __name__=="__main__":
    main()

