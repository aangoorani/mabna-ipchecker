from handlers import iphandler, inputhandler
import os
import json
import csv


pathgen = lambda *x: os.path.join(os.getcwd(), *x)

def test():
    ips = inputhandler.extract_ip('inputs/Source_05-05-2024_10-51-41.pdf')
    print(f'# ips: {len(ips)}\n***\n{ips[:10]}\n###########################')
    iphandler.check_ip(ips[:10], 'res.csv')


if __name__ == "__main__":
    test()
