import sys
import os

from argparse import ArgumentParser

parser = ArgumentParser(description="Run Quast for 10X data -- step2: Concatenate all quast alignment files together to generate file: all_alignments_supernova_contig-fasta.tsv")
parser.add_argument('--out_dir','-o_dir', help="Directory to store outputs", default='./Quast_results_for_10X/')

args = parser.parse_args()

if __name__ == "__main__":
    if len(sys.argv) == 1:
        os.system("python QuastXX_step2.py -h")
    else:
        if not os.path.exists(args.out_dir):
            os.system("mkdir " + args.out_dir)

        output = open('count_files.txt','r').read()
        num_files = int(output) - 1
        
        command_2 = "./cat_alignment_files.sh " + args.out_dir  + " " + str(num_files-1) 
        print(command_2)
        os.system(command_2)


        

        






