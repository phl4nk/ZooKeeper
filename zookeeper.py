#!/usr/bin/python
# ZooKeeper
# Logfile Malware harvester
# v.0.3

import sys,time,requests,re
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

SLEEP_TIME = 1

def check_args():
    if(len(sys.argv) != 3):
        print "Usage: ZooKeeper.py <log_file> <zoo_folder>\n\
e.g. ZooKeeper.py /var/log/apache2/access.log /tmp/zoo/";
        sys.exit(1)

# super naive approach, but does the job
# return first occurance of URI, or return empty string
def sniffForURL(string):
    # http://mail.python.org/pipermail/tutor/2002-September/017228.html
    regex = re.compile(r'\b(?:https?):[\w/#~:.?+=&%@!\-.:?\\-]+?(?=[.:?\-]*(?:[^\w/#~:.?+=&%@!\-.:?\-]|$))')
    match = regex.search(string)
    return match.group() if match is not None else ''

# continiously read from [log] file
# returns any new lines
# what about log_rotate?
def tail(file):
    global SLEEP_TIME
    while True:
        line = file.readline()
        if not line or not line.endswith('\n'):
            time.sleep(SLEEP_TIME)
            continue
        yield line

# downloads given URI, then saves it to folder from sys.argv
# updates knwon_links with URI to avoid duplicate downloads [regardless of download status]
# doesn't return anything, just gives up if any fart of an error arrises
def handleResource(URI):
    try:
        print "[+] Attempting to download:", URI
        # save in known_links to avoid duplicate
        with open('./known_links', 'a+') as f:
            f.write(URI+'\n')
        # Download the link
        response = requests.get(URI,verify=False,timeout=8)
        # dont dowload common error codes,
        if response.status_code not in [400,401,403,404,500,502,503,504]:
            print "[+] Saving resource"
            # quick replace for filename for unix dirs
            with open(str(sys.argv[2])+URI.replace('/','_'), 'wb') as f:
                f.write(response.content)
        else:
            print "[!] Not saving, Got bad status code:", response.status_code
    except Exception as e:
        print "[!] Something went wrong", e
        pass

# checks the known_links file for duplicate entry
# returns 1 if dupe is found, 0 if not
def isDupe(link):
    f = open('./known_links','r')
    ret_code = 0
    for line in f:
        if link == line.rstrip("\n"):
            print "[!] Duplicate link, not re-downloading"
            ret_code = 1
            break
    f.close()
    return ret_code

# Main controller
def ZooKeeper():
    print "[+] Starting to watch Log file:", sys.argv[1]
    for line in tail(open(sys.argv[1], 'r')):
        url = sniffForURL(line)
        if url and not isDupe(url):
            handleResource(url)

if __name__ == '__main__':
    check_args()
    ZooKeeper()
