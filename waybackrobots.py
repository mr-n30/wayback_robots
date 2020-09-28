#!/usr/bin/env python3
import json
import argparse
import requests
from functools import partial
from multiprocessing import Pool

# Parse cmd line arguments
parser = argparse.ArgumentParser(description="Fetch a given sites robots.txt file from https://web.archive.org/")
#group = parser.add_mutually_exclusive_group()
parser.add_argument("domain", help="Domain to fetch (Can be *.example.com)")
parser.add_argument("-t", "--threads", help="Number of concurrent processes (Default 5)", type=int, default=5)
parser.add_argument("-v", "--verbose", help="Increase verbosity", action="store_true")
parser.add_argument("-o", "--output", help="File to write output to")
args = parser.parse_args()

domain  = args.domain
threads = args.threads
verbose = args.verbose
output  = args.output

def write_to_file(text, check):
  f = open(output, "a+")
  if not check:
    f.write(text)
  else:
    f.close()


# User-Agent
headers = {
  "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36"
}

def wayback_robots(json_data):
  timestamp = json_data[0]
  url       = json_data[1]
  try:
    r = requests.get(f"https://web.archive.org/web/{timestamp}/{url}")
    if args.verbose:
      print(r.text)
    if "<" in r.text or ">":
      pass
    else:
      if output:
        write_to_file(r.text, 0)
      print(f"Trying: https://web.archive.org/web/{timestamp}/{url}")
  except:
    pass

def load_data():
  r = requests.get(f"https://web.archive.org/cdx/search/cdx?url={domain}/robots.txt&output=json&fl=timestamp,original&filter=statuscode:200&collapse=digest")
  json_data = json.loads(r.text)
  return json_data[1::]

if __name__ == "__main__":
  data = load_data()
  with Pool(threads) as p:
    p.map(wayback_robots, data)
    if output:
      write_to_file(text='', check=1)
    print("[+] Done...")
