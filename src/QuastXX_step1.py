import sys
import os

from argparse import ArgumentParser

parser = ArgumentParser(description="Run Quast for 10X data -- step1: Split WGS contig file to multiple small files (maximum 100 files, so make sure total_lines_of_WGS_contig_file/lines <= 100), and run Quast separately")
parser.add_argument('--lines','-l',type=int,help="line number for each small contig file", default=10000)
parser.add_argument('--input_file','-i',help="Input contig filename")
parser.add_argument('--out_dir','-o_dir', help="Directory to store outputs", default='./Quast_results_for_10X/')
parser.add_argument('--reference','-r', help="Referece fasta file")

args = parser.parse_args()

if __name__ == "__main__":
    if len(sys.argv) == 1:
        os.system("chmod +x *.sh")
        os.system("python QuastXX_step1.py -h")
    else:
        os.system("chmod +x *.sh")
        if not os.path.exists(args.out_dir):
            os.system("mkdir " + args.out_dir)

        command_1= "split -l "  + str(args.lines) + " " + args.input_file  +  " "  +args.input_file 
        print(command_1)
        os.system(command_1)
        command_3 = "ls " + args.input_file + "* | wc -l > count_files.txt"
        os.system(command_3)
        output = open('count_files.txt','r').read()
        num_files = int(output) - 1
        
        command_4 = "./run_list_quast_by_sbatch.sh " + args.input_file + " " + args.out_dir  + " " + str(num_files-1) + " " + args.reference
        print(command_4)
        os.system(command_4)


        

        






