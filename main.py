from handlers import iphandler, inputhandler
import os
import json
import csv
import argparse


pathgen = lambda *x: os.path.join(os.getcwd(), *x)


def main():
    parser = argparse.ArgumentParser(description='Extract and check IPs')
    parser.add_argument('input_file', help='Input file path')
    parser.add_argument('-t', '--text', action='store_true', help='Input file is a text file')
    parser.add_argument('-o', '--output', default='res.csv', help='Output file path')
    args = parser.parse_args()
    
    
    is_text = True if args.text else False

    ips = inputhandler.extract_ip(args.input_file, is_text)
    print(f'# ips: {len(ips)}\n***\n{ips[:10]}\n###########################')
    iphandler.check_ip(ips, args.output)


def test():
    ips = inputhandler.extract_ip('inputs/Source_05-05-2024_10-51-41.pdf')
    print(f'# ips: {len(ips)}\n***\n{ips[:10]}\n###########################')
    iphandler.check_ip(ips[:10], 'res.csv')


if __name__ == "__main__":
    main()
