# Nessus-report
A Python script to identify and match vulnerabilities shared by different hosts. It will group hosts with the same vulnerabilities in the same row, separating host names with commas, and listing common ports per vulnerability.

**Note:** Only supports .csv files.
### How to install
```bash
pip install -r requirements.txt
```
### How to run
#### Single file
```bash
python3 main.py -f file.csv -o p -n output_File
```

#### Multiple files
```bash
python3 main.py -f file.csv file2.csv file3.csv -o p -n output_File
```
