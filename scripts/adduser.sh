#!/bin/bash
password="123456"
echo "552523" | sudo useradd -d /home/guest -m -s /bin/bash -g users guest
echo "552523" | sudo passwd guest <<eof
123456
123456
eof
