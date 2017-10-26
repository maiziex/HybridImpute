# HybridImpute
## Install:
```
git clone https://github.com/maiziex/HybridImpute.git
## Running The Code:
```

### 1. Basic 
```
from HybridImpute import *
Matrix_hybrid = HybridImpute(Matrix_incomplete)
```
### 2. To use additional information for `HybridImpute`, use optional arguments. <br />
For example: protein to protein interaction
```
matrix_hybrid = HybridImpute(Matrix_incomplete,optional="ProteinToProtein_feature.txt")
```

### 3. If the test set exists, use `Validate_HybridImpute` to produce RMSE, Pearson Correlation Coefficient between true values and predicted values. <br />
output: Matrix_Filled_by_HybridImpute.csv
```
python2 Validate_HybridImpute.py -i ../doc/160703_Ricin_GIscore_Matrix_RicinResistPhenotype.xls -s ricin_resist -row 79 -col 79 -p 0.4 -fea ../doc/Homology_feature_yeast20.txt -o_dir ../result/ 
```
```
usage: Validate_HybridImpute.py [-h] [--input_file_prefix INPUT_FILE_PREFIX]
                                [--sheet_name SHEET_NAME]
                                [--feature_file_prefix FEATURE_FILE_PREFIX]
                                [--row_num ROW_NUM] [--col_num COL_NUM]
                                [--missing_percent MISSING_PERCENT]
                                [--out_dir OUT_DIR]

Validating Results by HybridImpute

optional arguments:
  -h, --help            show this help message and exit
  --input_file_prefix INPUT_FILE_PREFIX, -i INPUT_FILE_PREFIX
                        Input file prefix
  --sheet_name SHEET_NAME, -s SHEET_NAME
                        Sheet name of Input file prefix
  --feature_file_prefix FEATURE_FILE_PREFIX, -fea FEATURE_FILE_PREFIX
                        Input file prefix
  --row_num ROW_NUM, -row ROW_NUM
                        Number of rows of the matrix
  --col_num COL_NUM, -col COL_NUM
                        Number of columns of the matrix
  --missing_percent MISSING_PERCENT, -p MISSING_PERCENT
                        Defined missing percent for the matrix
  --out_dir OUT_DIR, -o_dir OUT_DIR
                        Directory to store outputs
```

