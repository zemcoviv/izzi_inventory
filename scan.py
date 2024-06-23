import os

def run_masscan(network_range, output_file):
    os.system(f"masscan -p1-65535 {network_range} --rate=10000 -oX {output_file}")

def run_nmap(input_file, output_file):
    os.system(f"nmap -sS -sV -O -iL {input_file} -oX {output_file}")
