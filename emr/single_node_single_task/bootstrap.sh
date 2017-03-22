#!/bin/bash
set -ex

#sudo yum -y install python35 python35-pip python35-virtualenv python35-devel
#sudo alternatives --set python /usr/bin/python3.5
pip install pandas pandas-td --user --disable-pip-version-check
