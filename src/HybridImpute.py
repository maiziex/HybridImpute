import macau
from sklearn.metrics import r2_score
import xlrd
from collections import defaultdict
import pickle
import numpy as np
import random
import math
import csv
import os
import scipy.io
from scipy import stats
import matplotlib
matplotlib.use('Agg')
from os import system
import matplotlib.pyplot as plt
from fancyimpute import (
                         BiScaler,
                         KNN,
                         NuclearNormMinimization,
                         SoftImpute,
                         SimpleFill)
from argparse import ArgumentParser



def Get_missing_entries_idx_cv(X_incomplete):
    m,n = X_incomplete.shape
    idx = 0
    missing_entries_idx = []
    for i in range(m):
        for j in range(n):
            if np.isnan(X_incomplete[i,j]):
                missing_entries_idx.append(idx)
            idx += 1
    return missing_entries_idx


def Save_customized_test_matrix_for_bmf(missing_mask,gene_matrix,test_matrix,train_matrix):
    fw = open(test_matrix,"w")
    fw_2 = open(train_matrix,"w")
    fw.writelines("%%MatrixMarket matrix coordinate real general\n")
    fw_2.writelines("%%MatrixMarket matrix coordinate real general\n")
    m,n = missing_mask.shape
    fw.writelines(str(m) + "\t" + str(n) + "\t" + str(m*n) + "\n")
    fw_2.writelines(str(m) + "\t" + str(n) + "\t" + str(m*n) + "\n")
    count_xin = 0
    for i in range(m):
        for j in range(n):
            if missing_mask[i,j] == True:
                val = gene_matrix[i,j]
                fw.writelines(str(i+1)+"\t" + str(j+1) + "\t" + str(val) + "\n")
                count_xin += 1
            else:
                val = gene_matrix[i,j]
                fw_2.writelines(str(i+1)+"\t" + str(j+1) + "\t" + str(val) + "\n")

    fw.close()
    fw_2.close()


def Get_distribution(X):
    percentile = defaultdict(float)
    m,n = X.shape
    all_list = []
    for i in range(m):
        for j in range(n):
            if ~np.isnan(X[i,j]):
                all_list.append(X[i,j])
    percentile[10] = abs(np.percentile(all_list,10))
    percentile[5] = abs(np.percentile(all_list,5))
    percentile[2] = abs(np.percentile(all_list,2))
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.hist(all_list,color='blue')
    plt.xlabel('values of the matrix')
    plt.ylabel('Frequency')
    plt.savefig("hist_of_values_of_the_matrix.png")
    plt.close()
    return percentile


def Initialize_X_incomplete(X_incomplete,test_filename,train_filename):
    m,n = X_incomplete.shape
    missing_mask = np.zeros((m, n),dtype=bool)
    softImpute = SoftImpute(convergence_threshold=0.0001,max_iters=300)
    X = softImpute.complete(X_incomplete)
    count_miss = 0
    for i in range(m):
        for j in range(n):
            if np.isnan(X_incomplete[i,j]):
                missing_mask[i,j] = True
                count_miss += 1

    return (X,missing_mask,count_miss)


def softimpute_used(X,X_incomplete,missing_mask,count_miss):
    softImpute = SoftImpute(convergence_threshold=0.0001,max_iters=300)
    X_filled_softimpute_no_biscale = softImpute.complete(X_incomplete)
    """
    softImpute_no_biscale_mse = ((X_filled_softimpute_no_biscale[missing_mask] - X[missing_mask]) ** 2).mean()
    softImpute_no_biscale_rmse = np.sqrt(float(((X_filled_softimpute_no_biscale[missing_mask] - X[missing_mask]) ** 2).sum())/count_miss)
    print("SoftImpute without BiScale MSE: %f" % softImpute_no_biscale_mse)
    print("SoftImpute without BiScale RMSE: %f" % softImpute_no_biscale_rmse)
    """
    return X_filled_softimpute_no_biscale


def softimpute_used_for_cv(X,X_incomplete,missing_mask,count_miss,defined_missing_percent,limit1,limit2,percentile):
    softImpute = SoftImpute(convergence_threshold=0.0001,max_iters=300)
    X_filled_softimpute_no_biscale = softImpute.complete(X_incomplete)
    """
    softImpute_no_biscale_mse = ((X_filled_softimpute_no_biscale[missing_mask] - X[missing_mask]) ** 2).mean()
    softImpute_no_biscale_rmse = np.sqrt(float(((X_filled_softimpute_no_biscale[missing_mask] - X[missing_mask]) ** 2).sum())/count_miss)
    print("SoftImpute without BiScale MSE: %f" % softImpute_no_biscale_mse)
    print("SoftImpute without BiScale RMSE: %f" % softImpute_no_biscale_rmse)
    """
    rmse_percentile = defaultdict(float)
    y = X[missing_mask]
    y_predict = X_filled_softimpute_no_biscale[missing_mask]
    
    y_percentile = defaultdict(list)
    y_predict_percentile = defaultdict(list)
    y_percentile_arr = defaultdict()
    y_predict_percentile_arr = defaultdict()
    
    for m,n in zip(y,y_predict):
        if m < percentile[10] and m > percentile[10]*(-1):
            y_percentile[10].append(m)
            y_predict_percentile[10].append(n)

    y_percentile_arr[10] = np.asarray(y_percentile[10])
    y_predict_percentile_arr[10] = np.asarray(y_predict_percentile[10])
    rmse_percentile[10] = np.sqrt(float(((y_predict_percentile_arr[10] - y_percentile_arr[10]) ** 2).sum())/len(y_predict_percentile_arr[10]))
    
    for m,n in zip(y,y_predict):
        if abs(m) < percentile[5] and abs(m) > percentile[10]:
            y_percentile[5].append(m)
            y_predict_percentile[5].append(n)

    y_percentile_arr[5] = np.asarray(y_percentile[5])
    y_predict_percentile_arr[5] = np.asarray(y_predict_percentile[5])
    rmse_percentile[5] = np.sqrt(float(((y_predict_percentile_arr[5] - y_percentile_arr[5]) ** 2).sum())/len(y_predict_percentile_arr[5]))

    for m,n in zip(y,y_predict):
        if abs(m) < percentile[2] and abs(m) > percentile[5]:
            y_percentile[2].append(m)
            y_predict_percentile[2].append(n)

    y_percentile_arr[2] = np.asarray(y_percentile[2])
    y_predict_percentile_arr[2] = np.asarray(y_predict_percentile[2])
    rmse_percentile[2] = np.sqrt(float(((y_predict_percentile_arr[2] - y_percentile_arr[2]) ** 2).sum())/len(y_predict_percentile_arr[2]))

    return (X_filled_softimpute_no_biscale, rmse_percentile)


def bmf_used(test_filename,train_filename,X,X_incomplete,add_SI):
    SI = Create_pearson_feature(X_incomplete, add_SI)
    test_set = scipy.io.mmread(test_filename)
    train_set = scipy.io.mmread(train_filename)
    result = macau.macau(Y=train_set,Ytest=test_set,num_latent=32,precision="adaptive",burnin=200,nsamples=100)
    result_SI = macau.macau(Y = train_set,Ytest=test_set,side=[SI,SI],num_latent=32,precision="adaptive",burnin=200,nsamples=100)
    """
    print result
    print result_SI
    results = result.prediction
    y = results['y'].values.tolist()
    y_predict = results['y_pred'].values.tolist()
    print("corrcoef:")
    print(np.corrcoef(y,y_predict))
    slope, intercept, r_value, p_value, std_err = stats.linregress(y,y_predict)
    print(r_value)
    """

    """
    results_SI = result_SI.prediction
    y_SI = results_SI['y'].values.tolist()
    y_SI_predict = results_SI['y_pred'].values.tolist()
    print("corrcoef for SI:")
    print(np.corrcoef(y_SI,y_SI_predict))
    slope, intercept, r_value, p_value, std_err = stats.linregress(y_SI,y_SI_predict)
    print(r_value**2)
    print("rmse")
    rmse = np.sqrt(float(((np.asarray(y) - np.asarray(y_predict)) ** 2).sum())/len(y))
    print(rmse)
    print("rmse with ppc")
    rmse_ppc = np.sqrt(float(((np.asarray(y_SI) - np.asarray(y_SI_predict)) ** 2).sum())/len(y_SI))
    print(rmse_ppc)
    """
    os.system('rm feature_pp.mm')
    os.system('rm temp.mm')
    os.system('rm temp_feature.mm')
    
    return result, result_SI


def bmf_used_for_cv(test_filename,train_filename,X,X_incomplete,percentile):
    test_set = scipy.io.mmread(test_filename)
    train_set = scipy.io.mmread(train_filename)
    result = macau.macau(Y=train_set,Ytest=test_set,num_latent=32,precision="adaptive",burnin=200,nsamples=100)
    results = result.prediction
    y = results['y'].values.tolist()
    y_predict = results['y_pred'].values.tolist()
    """
    print("corrcoef:")
    print(np.corrcoef(y,y_predict))
    slope, intercept, r_value, p_value, std_err = stats.linregress(y,y_predict)
    print(r_value)
    """
    rmse_percentile = defaultdict(float)
    y_percentile = defaultdict(list)
    y_predict_percentile = defaultdict(list)
    y_percentile_arr = defaultdict()
    y_predict_percentile_arr = defaultdict()
    for m,n in zip(y,y_predict):
        if m < percentile[10] and m > percentile[10]*(-1):
            y_percentile[10].append(m)
            y_predict_percentile[10].append(n)

    y_percentile_arr[10] = np.asarray(y_percentile[10])
    y_predict_percentile_arr[10] = np.asarray(y_predict_percentile[10])
    rmse_percentile[10] = np.sqrt(float(((y_predict_percentile_arr[10] - y_percentile_arr[10]) ** 2).sum())/len(y_predict_percentile_arr[10]))

    for m,n in zip(y,y_predict):
        if abs(m) < percentile[5] and abs(m) > percentile[10]:
            y_percentile[5].append(m)
            y_predict_percentile[5].append(n)

    y_percentile_arr[5] = np.asarray(y_percentile[5])
    y_predict_percentile_arr[5] = np.asarray(y_predict_percentile[5])
    rmse_percentile[5] = np.sqrt(float(((y_predict_percentile_arr[5] - y_percentile_arr[5]) ** 2).sum())/len(y_predict_percentile_arr[5]))

    for m,n in zip(y,y_predict):
        if abs(m) < percentile[2] and abs(m) > percentile[5]:
            y_percentile[2].append(m)
            y_predict_percentile[2].append(n)

    y_percentile_arr[2] = np.asarray(y_percentile[2])
    y_predict_percentile_arr[2] = np.asarray(y_predict_percentile[2])
    rmse_percentile[2] = np.sqrt(float(((y_predict_percentile_arr[2] - y_percentile_arr[2]) ** 2).sum())/len(y_predict_percentile_arr[2]))
    os.system('rm test_cv_matrix_for_bmf_missingpercent.mm')
    os.system('rm train_cv_matrix_for_bmf_missingpercent.mm')
    return (result, rmse_percentile)


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


def CenterCosine(X_incomplete):
    m,n = X_incomplete.shape
    X_centercosine = X_incomplete.copy()
    for i in range(m):
        for j in range(n):
            if np.isnan(X_centercosine[i,j]):
                X_centercosine[i,j] = 0 - np.nanmean(X_incomplete[i])
            else:
                X_centercosine[i,j] = X_centercosine[i,j] - np.nanmean(X_incomplete[i])

    return X_centercosine


def Create_pearson_feature(X_incomplete,add_SI):
    """ make a PPI_SI_dict_raw only based on origin X_incomplete  """
    filename =  "temp_feature.mm"
    fw = open(filename,"w")
    count_all = 0
    m,n = X_incomplete.shape
    PPI_SI_dict_raw = defaultdict(lambda: defaultdict(list))
    all_pearsoncor = []
    X_centercosine = CenterCosine(X_incomplete)
    for i in range(m):
        for j in range(n):
            if i != j:
                vector_i = X_centercosine[i]
                vector_j = X_centercosine[j]
                pearsoncor = sum([a*b for a,b in zip(vector_i,vector_j)])/(np.sqrt(sum([a**2 for a in vector_i]))*np.sqrt(sum([b**2 for b in vector_j])))
                all_pearsoncor.append(pearsoncor)
                if pearsoncor >= 0.1: 
                    fw.writelines(str(i+1) + "\t" + str(j+1) + "\t" + "1" + "\n")
                    PPI_SI_dict_raw[i][j] = pearsoncor
                    count_all += 1

    fw.close()
    fw =  open("temp.mm","w")
    fw.writelines("%%MatrixMarket matrix coordinate real general\n")
    fw.writelines(str(m) + "\t" + str(n) + "\t" + str(count_all) + "\n")
    fw.close()
    if add_SI != 'No':
        system("cat temp.mm " +  add_SI + " temp_feature.mm > feature_pp.mm")
    else:
        system("cat temp.mm temp_feature.mm > feature_pp.mm")
    
    SI = scipy.io.mmread("feature_pp.mm")
    return SI


def CrossValidation(X_incomplete,percentile):
    bmf_percentile_weight = defaultdict(float)
    softimpute_percentile_weight = defaultdict(float)
    m,n = X_incomplete.shape    
    missing_entries_idx_cv = Get_missing_entries_idx_cv(X_incomplete)
    missing_percent_cv = 0.1
    test_filename_cv = "test_cv_matrix_for_bmf_missingpercent.mm"
    train_filename_cv = "train_cv_matrix_for_bmf_missingpercent.mm"
    rand_num_one_per_row_cv = Get_rand_num_one_per_row(m,n,missing_entries_idx_cv)
    X_incomplete_cv,missing_mask_cv,count_miss_cv = RandomlySampling_TestSet(X_incomplete,missing_entries_idx_cv,missing_percent_cv,rand_num_one_per_row_cv)
    Save_customized_test_matrix_for_bmf(missing_mask_cv,X_incomplete,test_filename_cv,train_filename_cv)
    X_filled_softimpute_no_biscale_cv,softimpute_rmse_percentile = softimpute_used_for_cv(X_incomplete,X_incomplete_cv,missing_mask_cv,count_miss_cv,missing_percent_cv,-1,1,percentile)
    bmf_result_cv, bmf_rmse_percentile = bmf_used_for_cv(test_filename_cv,train_filename_cv,X_incomplete,X_incomplete_cv,percentile)
    if bmf_rmse_percentile[2] < softimpute_rmse_percentile[2]:
        bmf_percentile_weight[2] = 0.7
        softimpute_percentile_weight[2] = 0.3
    else:
        bmf_percentile_weight[2] = 0.3
        softimpute_percentile_weight[2] = 0.7
    if bmf_rmse_percentile[5] < softimpute_rmse_percentile[5]:
        bmf_percentile_weight[5] = 0.7
        softimpute_percentile_weight[5] = 0.3
    else:
        bmf_percentile_weight[5] = 0.3
        softimpute_percentile_weight[5] = 0.7
    if bmf_rmse_percentile[10] < softimpute_rmse_percentile[10]:
        bmf_percentile_weight[10] = 0.6
        softimpute_percentile_weight[10] = 0.4
    else:
        bmf_percentile_weight[10] = 0.4
        softimpute_percentile_weight[10] = 0.6


    return (bmf_percentile_weight,softimpute_percentile_weight)


def Hybrid(X,X_filled_softimpute_no_biscale,X_incomplete,missing_mask,bmf_result,test_filename,bmf_percentile_weight,softimpute_percentile_weight,percentile):
    X_hybrid = X_incomplete.copy()
    X_bmf = X_incomplete.copy()
    y1 = X[missing_mask]
    y1_predict = X_filled_softimpute_no_biscale[missing_mask]
    
    m,n = missing_mask.shape
    test1_set_dict = defaultdict()
    for i in range(m):
        for j in range(n):
            if missing_mask[i,j] == True:
                test1_set_dict[i,j] = float(X[i,j])

    y1_dict = defaultdict()
    y2_dict = defaultdict()
    for idx in range(len(y1)):
        y1_dict[y1[idx]] = y1_predict[idx]

    results = bmf_result.prediction
    y2 = results['y'].values.tolist()
    y2_predict = results['y_pred'].values.tolist()
    bmf_rmse = np.sqrt(float(((np.asarray(y2) - np.asarray(y2_predict)) ** 2).sum())/len(y2))
    """
    print("pearson correlation between y and y_predict")
    print(np.corrcoef(y2,y2_predict))
    slope, intercept, r_value, p_value, std_err = stats.linregress(y2,y2_predict)
    print(r_value)
    """

    f = open(test_filename,"r")
    count_line = 0
    test2_set_dict = defaultdict()
    for line in f:
        if count_line > 1:
            data = line.rsplit()
            test2_set_dict[int(data[0])-1,int(data[1])-1] = float(data[2])
        count_line += 1
    
    for idx in range(len(y2)):
        y2_dict[y2[idx]] = y2_predict[idx]

    y = []
    y_predict = []
    all_v1 = []
    all_v2 = []

    for key, value in test1_set_dict.items():
        value2 = test2_set_dict[key]
        if abs(round(value,4)) == abs(round(value2,4)) or abs(round(abs(round(value2,4)) -  abs(round(value,4)),4)) == 0.0001:
            v1 = y1_dict[value]
            v2 = y2_dict[value2]
            all_v1.append(v1)
            all_v2.append(v2)
            X_bmf[key] = v2
            y.append(value)
            if v1 < percentile[10] and v1 > percentile[10]*(-1):
                y_predict.append(v1*softimpute_percentile_weight[10]+v2*bmf_percentile_weight[10])
                X_hybrid[key] = v1*softimpute_percentile_weight[10]+v2*bmf_percentile_weight[10]
            elif abs(v1) < percentile[5] and abs(v1) > percentile[10]:
                y_predict.append(v1*softimpute_percentile_weight[5]+v2*bmf_percentile_weight[5])
                X_hybrid[key] = v1*softimpute_percentile_weight[5]+v2*bmf_percentile_weight[5]
            elif abs(v1) < percentile[2] and abs(v1) > percentile[5]:
                y_predict.append(v1*softimpute_percentile_weight[2]+v2*bmf_percentile_weight[2])
                X_hybrid[key] = v1*softimpute_percentile_weight[2]+v2*bmf_percentile_weight[2]
            else:
                y_predict.append(np.median([v1,v2]))
                X_hybrid[key] = np.median([v1,v2])

    y_predict_arr = np.asarray(y_predict)
    y_arr = np.asarray(y)
    combined_rmse = np.sqrt(float(((y_predict_arr - y_arr) ** 2).sum())/len(y_arr))
    """
    print("Combined RMSE: %f" % combined_rmse)
    print("pearson correlation between y and y_predict for combined algorithms:")
    print(np.corrcoef(y,y_predict))
    slope, intercept, r_value, p_value, std_err = stats.linregress(y,y_predict)
    print(r_value)
    
    print("pearson correlation between softimpute_predict and bmf_predict:")
    print(np.corrcoef(all_v1,all_v2))
    slope, intercept, r_value, p_value, std_err = stats.linregress(all_v1,all_v2)
    print(r_value)
    """
    os.system('rm test_matrix_for_bmf_missingpercent.mm')
    os.system('rm train_matrix_for_bmf_missingpercent.mm')
    return (bmf_rmse,combined_rmse, np.corrcoef(y,y_predict),len(y), X_bmf, X_hybrid)



def HybridImpute(X_incomplete,*positional_parameters, **keyword_parameters):
    if 'optional' in keyword_parameters:
        option_flag = keyword_parameters['optional']
        print 'Adding Input Information for HybridImpute:', keyword_parameters['optional']
    else:
        option_flag = 0
    
    test_filename = "test_matrix_for_bmf_missingpercent.mm"
    train_filename = "train_matrix_for_bmf_missingpercent.mm"
    X,missing_mask,count_miss = Initialize_X_incomplete(X_incomplete,test_filename,train_filename)
    Save_customized_test_matrix_for_bmf(missing_mask,X,test_filename,train_filename)
  
    # cross validation to assign weight to each algorithm
    percentile = Get_distribution(X_incomplete)
    bmf_percentile_weight,softimpute_percentile_weight = CrossValidation(X_incomplete,percentile)
    
    X_filled_softimpute_no_biscale = softimpute_used(X,X_incomplete,missing_mask,count_miss)
    
    if option_flag == None or option_flag == 0:
        add_SI = 'No'
    else:
        add_SI = keyword_parameters['optional']
    

    bmf_result,bmf_result_SI = bmf_used(test_filename,train_filename,X,X_incomplete,add_SI)
    bmf_rmse,combined_rmse,ppc,num_test, X_bmf, X_hybrid = Hybrid(X,X_filled_softimpute_no_biscale,X_incomplete,missing_mask,bmf_result_SI,test_filename,bmf_percentile_weight,softimpute_percentile_weight,percentile)
    
    return X_hybrid, X_filled_softimpute_no_biscale, X_bmf


















        
