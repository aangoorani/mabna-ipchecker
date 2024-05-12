
import tabula 
import os
import json
import csv
from io import StringIO



def extract_ip(input_path, is_text=False):
    """
    Extract the Ip addresses from the pdf report and return a list of ip addresses.
    """

    if is_text:
        return list(set(extract_ip_from_txt(input_path)))

    # Read PDF File 
    # this contain a list 
    df = tabula.read_pdf(input_path, pages='1')[0]
    
    csv_buf = StringIO()
    csv_buf.seek(0)

    # Convert into Excel File 
    df.to_csv(csv_buf)
    csv_buf.seek(0)

    ips = []
    row_num = 0

    for row in csv.reader(csv_buf):
        # print(row)
        if row_num != 0:
            try:
                ips.append(row[2])
            except IndexError:
                continue
        row_num += 1

    csv_buf.truncate(0)
    csv_buf.close()

    return ips


def extract_ip_from_txt(input_path):
    """
    Extract the Ip addresses from the txt report and return a list of ip addresses.
    """
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    ips = []
    for line in lines:
        if line:=line.strip():
            ips.append(line)
    return ips