set -x
filename=$1
out_dir=$2
num=$3
ref=$4
declare -a arr=("aa" "ab" "ac" "ad" "ae" "af" "ag" "ah" "ai" "aj" "ak" "al" "am" "an" "ao" "ap" "aq" "ar" "as" "at" "au" "av" "aw" "ax" "ay" "az" "ba" "bb" "bc" "bd" "be" "bf" "bg" "bh" "bi" "bj" "bk" "bl" "bm" "bn" "bo" "bp" "bq" "br" "bs" "bt" "bu" "bv" "bw" "bx" "by" "bz" "ca" "cb" "cc" "cd" "ce" "cf" "cg" "ch" "ci" "cj" "ck" "cl" "cm" "cn" "co" "cp" "cq" "cr" "cs" "ct" "cu" "cv" "cw" "cx" "cy" "cz" "da" "db" "dc" "dd" "de" "df" "dg" "dh" "di" "dj" "dk" "dl" "dm" "dn" "do" "dp" "dq" "dr" "ds" "dt" "du" "dv")
start=0
for j in `eval echo {$start..$num}`
do
    echo ${arr[$j]}
    i=${arr[$j]}
    cp submit_quast.sbatch submit_quast_"$i".sbatch
    echo quast.py --extensive-mis-size 100 --threads 40 --fast --no-snps $filename"$i" -R $ref --fast -o $out_dir"quast_result_"$i>>submit_quast_"$i".sbatch
    sbatch submit_quast_"$i".sbatch
done

