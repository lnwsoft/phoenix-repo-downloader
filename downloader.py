# SAP Package Downloader based on the SAP DLM API
# Based on the work for https://github.com/Azure/sap-hana/blob/master/deploy/python/downloader/SAP_DLM.py
import argparse
import re
import requests
from requests.adapters import HTTPAdapter
from requests.auth import HTTPBasicAuth
from tqdm import tqdm
import math
import os

# Packages are list of files that need to be downloaded
# They should be normal SAP Download URLs, that can be generated in the
# SAP support launchpad
PACKAGE_DIR = "%s/packages/" % os.path.dirname(os.path.abspath(__file__))

resp_timeout_sec = 10

class HTTPSession(requests.Session):
    def __init__(self, auth=None, headers=None, retry=5):
        super(HTTPSession, self).__init__()
        if auth:
            self.auth    = auth
        if headers:
            self.headers = headers
        #if Config.debug.proxies:
        #    self.proxies = Config.debug.proxies
        #if Config.debug.cert:
        #    self.verify  = Config.debug.cert
        adapter = HTTPAdapter(max_retries=retry)
        self.mount("http://", adapter)
        self.mount("https://", adapter)

parser = argparse.ArgumentParser(description='Download SAP packages for LNW-Soft Project Phoenix')
parser.add_argument('--user', '-u', help = "SAP S-User", required=True)
parser.add_argument('--password', '-p', help = "SAP S-User Password", required=True)
parser.add_argument('--test', '-t', help = "Test package availability, do not download", action='store_true')
parser.add_argument('--package', '-P', help = "Package to download", required=True)
parser.add_argument('--target', '-T', help = "Target directory for download", default="./repository")
args = parser.parse_args()

s_user = args.user
s_password = args.password
url_file = "%s/%s.lst" % (PACKAGE_DIR, args.package)
dry_run = args.test

with open(url_file,"r") as f:
  urls = f.readlines()

ids = [url.strip().split("/")[-1] for url in urls if url.startswith("https://")]

print("Found %s files in package %s" % (len(ids), args.package))

if not args.test and not os.path.isdir(args.target):
    print("Target directory %s does not exist, and will be created." % args.target)
    os.mkdir(args.target)

repo_package_dir = "%s/%s" % (args.target, args.package)
if not args.test and not os.path.isdir(repo_package_dir):
    os.mkdir(repo_package_dir)

sess = HTTPSession(auth= HTTPBasicAuth(s_user, s_password), headers = { "User-Agent": "SAP Download Manager"})

url_token = "https://origin.softwaredownloads.sap.com/tokengen/"


for id in ids:
    payload = { "file": id }
    resp = sess.get(url_token, params=payload, timeout=resp_timeout_sec, stream=True)
    if not "content-disposition" in resp.headers:
        print("error with id %s" % id)
        continue
    disposition = resp.headers["content-disposition"]
    if disposition.find('filename="') < 0:
        print("error with id %s" % id)
        continue
    filename    = re.search("\"(.*?)\"",disposition).group(1)

    if args.package == "hostagent":
        if filename.startswith("SAPCAR"):
            filename = "SAPCAR"
        else if filename.startswith("SAPHOSTAGENT"):
            filename = "SAPHOSTAGENT.SAR"
    else:
        target_final = "%s/%s" % (repo_package_dir,filename)

    if os.path.isfile(target_final):
        print("%s already downloaded" % filename)
        continue

    target_download = "%s.download" % target_final

    total_length = int(resp.headers.get('content-length'))

    if dry_run:
        print("%s - %s - %s - ok" % (id, filename, total_length))
    else:
        success = False
        with open(target_download, "wb") as f:
            try:
                for chunk in tqdm(resp.iter_content(chunk_size=1024), total = math.ceil(total_length/1024), desc = filename, unit = "kb"):
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)
                        f.flush()
                success = True
            except Exception as e:
                print("Exception %s happens, retry..." % e)
        if success:
            os.rename(target_download, target_final)
