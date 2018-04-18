#!/bin/sh

if [ -z $(which td) ]; then
  echo "You first need to install Treasure Data Toolbelt: http://toolbelt.treasuredata.com/"
  exit 1
fi

echo "You need to accept and agree with CRITEO LABS DATA TERM OF USE at: http://labs.criteo.com/2014/02/dataset/\n"
while true; do
  read -p "Have you accepted? [Y/n] " yn
  case $yn in
    [Yy]* ) break;;
    [Nn]* ) echo "Sorry, we cannot proceed unless you accept the term of use."; exit;;
    * ) echo "Invalid input. Try again...";;
  esac
done

curl -o criteo.tar.gz -L http://labs.criteo.com/wp-content/uploads/2015/04/dac_sample.tar.gz
mkdir criteo
tar xvzf criteo.tar.gz -C criteo
cd criteo

# insert row number to the first column
awk '{print NR "\t" $0}' dac_sample.txt > criteo.tsv

td db:create criteo_sample
td table:create criteo_sample samples
td import:auto \
  --format tsv \
  --columns rowid,label,i1,i2,i3,i4,i5,i6,i7,i8,i9,i10,i11,i12,i13,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,c15,c16,c17,c18,c19,c20,c21,c22,c23,c24,c25,c26 \
  --column-types long,int,int,int,int,int,int,int,int,int,int,int,int,int,int,string,string,string,string,string,string,string,string,string,string,string,string,string,string,string,string,string,string,string,string,string,string,string,string,string,string \
  --time-value `date +%s` \
  --auto-create criteo_sample.samples ./criteo.tsv

cd ..
rm criteo.tar.gz
rm -rf criteo
