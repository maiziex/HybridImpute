from os import system
import xlrd
from collections import defaultdict
import numpy as np
import random
import math
from scipy import stats
import os
from HybridImpute import *
import sys
import csv
from argparse import ArgumentParser


parser = ArgumentParser(description="Validating Results by HybridImpute")
parser.add_argument('--input_file_prefix','-i',help="Input file prefix")
parser.add_argument('--sheet_name','-s',help="Sheet name of Input file prefix")
parser.add_argument('--feature_file_prefix','-fea',help="Input file prefix")
parser.add_argument('--row_num','-row',help="Number of rows of the matrix")
parser.add_argument('--col_num','-col',help="Number of columns of the matrix")
parser.add_argument('--missing_percent','-p',help="Defined missing percent for the matrix")
parser.add_argument('--out_dir','-o_dir', help="Directory to store outputs", default='../results/')

args = parser.parse_args()

def read_matrix(input_file,sheetname,row,col):
    workbook = xlrd.open_workbook(input_file)
    sheet = workbook.sheet_by_name(sheetname)
    g_matrix = np.empty((row,col,))
    g_matrix[:] = np.NAN
    count_nan_raw = 0
    idx_num = 0
    origin_missing_entries = []
    missing_entries_idx = []
    max_value = 0
    min_value = 0
    all_values = []
    for i in range(row):
        for j in range(col):
            val = sheet.cell(i, j).value
            if val != "--":
                g_matrix[i,j] = val
                all_values.append(val)
                if max_value < val:
                    max_value = val
                if min_value > val:
                    min_value = val
            elif val.encode() == "--":
                count_nan_raw += 1
                origin_missing_entries.append([i,j])
                missing_entries_idx.append(idx_num)
            idx_num += 1

    return(g_matrix,count_nan_raw,missing_entries_idx)


def Get_rand_num_one_per_row(m,n,missing_entries_idx):
    # make sure at least leaving one element for each row
    all_row = []
    count_idx = 0
    rand_num_one_per_row = []
    for i in range(m):
        for j in range(n):
            all_row.append(count_idx)
            count_idx += 1
        
        all_row_no_missing = list(set(all_row)-set(missing_entries_idx))
        rand_num_one_per_row.append(random.sample(all_row_no_missing,1)[0])
        all_row = []
    
    return rand_num_one_per_row


def RandomlySampling_TestSet(X,missing_entries_idx,defined_missing_percent,rand_num_one_per_row):
    m,n = X.shape
    missing_mask = np.ones((m, n),dtype=bool)
    all_num_raw = []
    for i in range(m*n):
        all_num_raw.append(i)
    
    all_num = list(set(all_num_raw) - set(missing_entries_idx)-set(rand_num_one_per_row))
    percent_missing = float(defined_missing_percent*m*n)/len(all_num)
    rand_num = random.sample(all_num,int(math.ceil(percent_missing*len(all_num))))
    sorted_rand_num = sorted(rand_num)
    X_incomplete = X.copy()
    idx_num = 0
    curr_idx = 0
    count_miss = 0
    for i in range(m):
        for j in range(n):
            try:
                if idx_num == sorted_rand_num[curr_idx]:
                    idx_num += 1
                    curr_idx += 1
                    X_incomplete[i,j] = np.NAN
                    count_miss += 1
                else:
                    missing_mask[i,j] = False
                    idx_num += 1
            except:
                missing_mask[i,j] = False
                idx_num += 1

    return (X_incomplete,missing_mask,count_miss)


def plot_missing_value(X,X_filled,missing_mask,missing_percent,fig_name,out_dir):
    y = list(X[missing_mask])
    y_predict = list(X_filled[missing_mask])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.scatter(y,y_predict)
    plt.plot([-100, 100],[-100, 100],'k--',label="Best Fit")
    legend = ax.legend(loc='upper left', shadow=True)
    plt.xlabel('value_true')
    plt.ylabel('value_predict')
    ax.set_title('missing percent %3.2f%%' % (int(missing_percent*100)))
    if os.path.exists(out_dir):
        print("Save figures to " + out_dir)
    else:
        os.system('mkdir ' + out_dir)
    plt.savefig(out_dir + "/scatter_" + fig_name + ".png")
    plt.close()


def write_matrix_to_csv(X_filled,csv_file):
    f = open(csv_file, "w")
    writer = csv.writer(f)
    for values in X_filled:
        writer.writerow(values)
    f.close()

def print_rmse(X_raw,X_filled,missing_mask_raw,count_miss_raw,fig_name,out_dir):
    rmse_filled = np.sqrt(float(((X_raw[missing_mask_raw] - X_filled[missing_mask_raw]) ** 2).sum())/count_miss_raw)
    plot_missing_value(X_raw,X_filled,missing_mask_raw,defined_missing_percent,fig_name,out_dir)
    print("RMSE_" + fig_name  + ":")
    print(rmse_filled)
    slope, intercept, r_value, p_value, std_err = stats.linregress(X_raw[missing_mask_raw],X_filled[missing_mask_raw])
    print("Pearson Correlation Coefficient_" + fig_name + ":")
    print(r_value)
    return rmse_filled


if __name__ == "__main__":
    if len(sys.argv) == 1:
        os.system("python Validate_HybridImpute.py -h")
    else:
        defined_missing_percent = float(args.missing_percent)
        X_raw,count_nan_raw,missing_entries_idx = read_matrix(args.input_file_prefix,args.sheet_name,int(args.row_num),int(args.col_num))
        m,n = X_raw.shape
        rand_num_one_per_row = Get_rand_num_one_per_row(m,n,missing_entries_idx)
        X_incomplete,missing_mask_raw,count_miss_raw = RandomlySampling_TestSet(X_raw,missing_entries_idx,defined_missing_percent,rand_num_one_per_row)
        X_hybrid, X_filled_softimpute_no_biscale, X_bmf = HybridImpute(X_incomplete,optional=args.feature_file_prefix)
        print("Final Results:")
        rmse_hybrid = print_rmse(X_raw,X_hybrid,missing_mask_raw,count_miss_raw,'hybrid',args.out_dir)
        write_matrix_to_csv(X_hybrid,args.out_dir+ 'Matrix_Filled_by_HybridImpute.csv')


