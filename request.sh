#!/bin/bash

for i in {1..11000}
do
    curl -s \
    -H "Host: 192.168.159.152:5000"\
    -H "User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0"\
    -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"\
    -H "Accept-Language: en-US,en;q=0.5"\
    -H "Accept-Encoding: gzip, deflate"\
    -H "Connection: keep-alive"\
    -H "Upgrade-Insecure-Requests: 1"\
    -H "Cache-Control: max-age=0"\
    --proxy http://192.168.159.57:12345 \
    http://192.168.159.152:5000
done