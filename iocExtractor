#!/bin/python3

import json
import argparse
import csv
import json
import pdfplumber
import re
import os
import requests

#IOC Regexes
md5_pattern = re.compile(r"(?<![0-9a-f])[0-9a-f]{32}(?![0-9a-f])")
sha1_pattern = re.compile(r"(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])")
sha256_pattern = re.compile(r"(?<![0-9a-f])[0-9a-f]{64}(?![0-9a-f])")
sha512_pattern = re.compile(r"[0-9a-f]{128}")
ipv4_pattern = re.compile(r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}")
domain_pattern = re.compile(r"(?:[A-Za-z0-9\-]+\.)+[A-Za-z]{2,}")
url_pattern = re.compile(r"https?://(?:[A-Za-z0-9\-]+\.)+[A-Za-z0-9]{2,}(?::\d{1,5})?[A-Za-z0-9\-%?=\+\.]+")

def get_iocs(data):
    results = {}
    results = {
        "md5": list(set(md5_pattern.findall(data))),
        "sha1": list(set(sha1_pattern.findall(data))),
        "sha256": list(set(sha256_pattern.findall(data))),
        "sha512": list(set(sha512_pattern.findall(data))),
        "ipv4": list(set(ipv4_pattern.findall(data))),
        "domain": list(set(domain_pattern.findall(data))),
        "url": list(set(url_pattern.findall(data)))
    }
    return results


def deliver_csv_output(file_name, iocs_file):
    with open("csv_output", "a") as f:
        data = f.write("filename, type, value")
        data = f.write("\n")
        for iocs, value in iocs_file.items():
            for i in value:
                data = f.write(f"{file_name}, {iocs}, {i}\n")


def deliver_json_output():
    pass


if __name__=='__main__':

    parser = argparse.ArgumentParser(description="Extract IoC from Different types of files.")
    parser.add_argument('-v', '--verbose', metavar='<on/off>', default='off', help='')
    parser.add_argument('-o', '--output', metavar='', help='')
    parser.add_argument('--pdf', metavar='', help='')
    parser.add_argument('--text', metavar='', help='')
    args = parser.parse_args()

    if args.pdf:
        try:
            with pdfplumber.open(args.pdf) as pdf:
                pdf_pages = pdf.pages
                full_data_stream = ""
                for page in pdf_pages:
                    text_data = page.extract_text()
                    full_data_stream = full_data_stream + "".join(text_data)
                pdf_iocs = get_iocs(full_data_stream)
                deliver_csv_output(args.pdf, pdf_iocs)
                if args.verbose == 'on':
                    print(pdf_iocs)
                else:
                    pass
        except:
            print("Your file is not a PDF.")
    elif args.text:
        with open(args.text, 'r') as f:
            data_stream = f.read()
            text_iocs = get_iocs(data_stream)
            deliver_csv_output(args.text, text_iocs)
            if args.verbose == 'on':
                print(text_iocs)
    else:
        pass
