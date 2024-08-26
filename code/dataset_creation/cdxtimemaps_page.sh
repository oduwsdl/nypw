#!/usr/bin/env bash

CDXAPI="http://web.archive.org/cdx/search/cdx"

count=0

while read -r line
do
  let count++
  p=$(curl -sGD tmp_$1.txt --data-urlencode "url=$line" --data-urlencode "showNumPages=true" $CDXAPI)
  echo "$line" >> cdxhttpres_$1.txt
  cat tmp_$1.txt >> cdxhttpres_$1.txt
  for i in $(seq 0 $p)
  do
    curl -sGD tmp_$1.txt --data-urlencode "url=$line" --data-urlencode "page=$i" $CDXAPI | awk -v prefix="$line" '{print prefix" "$0}' >> TM_$1_$count.txt
    status=$(grep ^"HTTP" tmp_$1.txt | tail -1| cut -d" " -f2)
    if [[ $status -ne 200 ]]
    then
      echo "$line $status $i" >> error_log_$1.txt
      if [[ $status -eq 503 ]]
      then
        sleep 1m
        continue
      fi
    fi
    rm tmp_$1.txt
  done
done <  $1
