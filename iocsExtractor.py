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
syscall_pattern = re.compile(r"[A-Z]{1,4}[a-z][A-Za-z]+")
domain_pattern = re.compile(r"(?:[A-Za-z0-9\-]+\.)+[A-Za-z]{2,}")
url_pattern = re.compile(r"https?://(?:[A-Za-z0-9\-]+\.)+[A-Za-z0-9]{2,}(?::\d{1,5})?[/A-Za-z0-9\-%?=\+\.]+")

def get_iocs(data):
    results = {}
    results = {
        "md5": list(set(md5_pattern.findall(data))),
        "sha1": list(set(sha1_pattern.findall(data))),
        "sha256": list(set(sha256_pattern.findall(data))),
        "sha512": list(set(sha512_pattern.findall(data))),
        "ipv4": list(set(ipv4_pattern.findall(data))),
        "possible_syscall": list(set(syscall_pattern.findall(data))),
        "domain": list(set(domain_pattern.findall(data))),
        "url": list(set(url_pattern.findall(data)))
    }
    return results


def deliver_csv_output(file_name, iocs_file):
    with open(args.output, "a") as f:
        data = f.write("filename, type, value")
        data = f.write("\n")
        for iocs, value in iocs_file.items():
            for i in value:
                data = f.write(f"{file_name}, {iocs}, {i}\n")


def deliver_json_output():
    pass


if __name__=='__main__':

    parser = argparse.ArgumentParser(description="Extract IoC from Different types of files.")
    parser.add_argument('-v', '--verbose', metavar='<on/off>', default='on', help='sets the output to be verbose. (default = on)')
    parser.add_argument('-o', '--output', metavar='<output_name>', help='sets the output file.')
    parser.add_argument('-f', '--file', metavar='<file>', help='sets a file as target.')
    args = parser.parse_args()
 
    if args.file:
        try:
            with pdfplumber.open(args.file) as pdf:
                pdf_pages = pdf.pages
                full_data_stream = ""
                for page in pdf_pages:
                    text_data = page.extract_text()
                    full_data_stream = full_data_stream + "".join(text_data)
                pdf_iocs = get_iocs(full_data_stream)
                if not args.output and args.verbose == 'on':
                    print(f"IoC from File {args.file}:")
                    for iocs, value in pdf_iocs.items():
                        for i in value:
                            print(f"\t{iocs}, {i}\t")
                else:
                    deliver_csv_output(args.file, pdf_iocs) 
        except:
            with open(args.file, 'r') as f:
                data_stream = f.read()
                text_iocs = get_iocs(data_stream)
                if not args.output and args.verbose == 'on':
                    print(f"IoC from File {args.file}:")
                    for iocs, value in text_iocs.items():
                        for i in value:
                            print(f"\t{iocs}, {i}\t")
                else:
                    deliver_csv_output(args.file, text_iocs)
