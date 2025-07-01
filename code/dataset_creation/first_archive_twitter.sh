#!/usr/bin/env bash
# Author: Kritika Garg
# Date: Dec 27, 2021
# Description: Randomly samples Twitter URLs, queries the CDX API for the first archive date, 
# and counts URLs for years 2016–2021 until at least 20 per year are collected.

CDXAPI="http://web.archive.org/cdx/search/cdx"

c21=0
c20=0
c19=0
c18=0
c17=0
c16=0

while read -r line
do
  idx=$(curl -sGD header_tmp_$1.txt -d "limit=1" --data-urlencode "url=$line" $CDXAPI)
  echo "$line" >> cdx_httpresponse_$1.txt
  cat header_tmp_$1.txt >> cdx_httpresponse_$1.txt
  status=$(grep ^"HTTP" header_tmp_$1.txt | tail -1| cut -d" " -f2)
  if [[ $status -eq 200 ]]
  then
    idx="${idx:=- - - - - - -}"
    echo "$line ${idx/*Blocked Site Error/X X X X X X X}" >> "$2_$1.txt"
    yr=$(echo $idx| awk '{print substr($2, 1, 4)}')
    if [[ "$yr" == 2021 ]]; then c21=$((c21+1)); fi
    if [[ "$yr" == 2020 ]]; then c20=$((c20+1)); fi
    if [[ "$yr" == 2019 ]]; then c19=$((c19+1)); fi
    if [[ "$yr" == 2018 ]]; then c18=$((c18+1)); fi
    if [[ "$yr" == 2017 ]]; then c17=$((c17+1)); fi
    if [[ "$yr" == 2016 ]]; then c16=$((c16+1)); fi
    echo "c21:$c21 c20:$c20 c19:$c19 c18:$c18 c17:$c17 c16:$c16"
  else
    echo "$line $status" >> error_log_$1.txt
    if [[ $status -eq 503 ]]; then sleep 1m; continue; fi
  fi
  if [[ ( $c21 -ge 20 && $c20 -ge 20 && $c19 -ge 20 && $c18 -ge 20 && $c17 -ge 20 && $c16 -ge 20 ) ]]; then break ; fi
done <  $1
