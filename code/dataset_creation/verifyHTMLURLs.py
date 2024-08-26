#!/usr/bin/env python3
import re, os, sys
from urllib.parse import urlparse
import validators, signal
import tldextract

part = sys.argv[3]
file = open(sys.argv[1], "r")
out_folder = sys.argv[2]
f_inv =  open(out_folder+'All.uniq_invurls_'+part,"w")
f_vh = open(out_folder+"All.uniq_valid.htmlurls_"+part, "w")
f_vnh = open(out_folder+"All.uniq_valid.nonhtmlurls_"+part, "w")


#accepted html extensions
regexes = ["\.[a-z]?html$", "\.php\d?$", "\.htm$", "\.asp$", "\.aspx$", "\.cgi$", "\.jsp$", "\.cfm$", "\.pl$", "\.do$"]
ext_reg_list = '(?:% s)' % '|'.join(regexes)


c=0

#timeout error
def timeout(signum, frame):
  raise TimeoutError


def validate_url(inp_url):
  signal.signal(signal.SIGALRM, timeout)
  signal.alarm(30)
  try:
    val = validators.url(inp_url)
  except TimeoutError:
    print("TE")
    val = False
  return val


for line in file:
  print(c)
  c+=1
  inp_url = line.strip()
#  print(inp_url)
  try:
    #validate URL
    val = validate_url(inp_url)
 #   print(val)

    if val:
      #get domain_info
      tld = tldextract.extract(inp_url)
      #get ext
      ext = (os.path.splitext(urlparse(inp_url).path)[1]).lower()
      #webpage or not
      webpage = False
      #trailing slash
      if 'robots.txt' not in inp_url:
        if ext == '':
          webpage = True
        elif re.match(ext_reg_list, ext):
          webpage = True
      if webpage:
        #save to file: valid_html
        f_vh.write(inp_url+"\t"+ext+"\t"+tld.subdomain+"\t"+tld.domain+"\t"+tld.suffix+"\n")
        #f_vh.write(f'{inp_url}\t{ext}\t{tld.subdomain}\t{tld.domain}\t{tld.suffix}\n')
      else:
        #save to file: valid_nonhtml
        f_vnh.write(inp_url+"\t"+ext+"\t"+tld.subdomain+"\t"+tld.domain+"\t"+tld.suffix+"\n")
#        f_vnh.write(f'{inp_url}\t{ext}\t{tld.subdomain}\t{tld.domain}\t{tld.suffix}\n')

    else:
      f_inv.write(inp_url+'\n')

  except Exception as e:
    print(e)
    f_inv.write(inp_url+'\n')
    continue


f_inv.close()
f_vh.close()
f_vnh.close()
