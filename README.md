# SAP Package Downloader for LNW-Soft Project Phoenix cloud deployments

## Quickstart
This will download the packages for S/4HANA 1909 and the HANA database installation to `./phoenix-repo-downloader/repository`. The contents of this directory then need to be uploaded into an Azure Storage account.

```
git clone https://github.com/lnwsoft/phoenix-repo-downloader
cd phoenix-repo-downloader
python3 -mvenv env
. env/bin/activate
pip install -r requirements.txt
./downloader.py --user <S-User> --password <S-User Password> --package hostagent
./downloader.py --user <S-User> --password <S-User Password> --package hana
./downloader.py --user <S-User> --password <S-User Password> --package s4hana-1909
```

## Futher information
* [Project Phoenix Documentation](http://docs.lnwsoft.com/projectphoenix/)
