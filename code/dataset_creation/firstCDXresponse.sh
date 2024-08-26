#!/usr/bin/env bash

CDXAPI="http://web.archive.org/cdx/search/cdx"

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
  else
    echo "$line $status" >> error_log_$1.txt
    if [[ $status -eq 503 ]]
    then
      sleep 1m
      continue
    fi
  fi
done <  $1