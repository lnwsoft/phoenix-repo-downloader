# SAP Package Downloader for LNW-Soft Project Phoenix cloud deployments

## Quickstart
This will download the packages for any LNW-Soft project Phoenix supported SAP system and HANA database installation to `./phoenix-repo-downloader/repository`. The contents of this directory then need to be uploaded into an Azure Storage Account.

```
git clone https://github.com/lnwsoft/phoenix-repo-downloader
cd phoenix-repo-downloader
python3 -mvenv env
. env/bin/activate
pip install -r requirements.txt
./downloader.py --user <S-User> --password <S-User Password> --package hostagent
./downloader.py --user <S-User> --password <S-User Password> --package hana
./downloader.py --user <S-User> --password <S-User Password> --package s4hana-1909
./downloader.py --user <S-User> --password <S-User Password> --package s4hana-2020
./downloader.py --user <S-User> --password <S-User Password> --package bw4hana-20
./downloader.py --user <S-User> --password <S-User Password> --package nw75-hdb
```

## Futher information
* [Project Phoenix Documentation](http://docs.lnwsoft.com/projectphoenix/)
