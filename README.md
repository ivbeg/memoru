# Memo_ru

Parser and data of lists.memo.ru website (database of victims of soviet repressions)
This project is incomplete and under heavy development.

Contact - ibegtin (at) gmail.com

## Setting Up

Install included dependencies

```bash
pip install pyparsing
pip install lxml
pip install pymongo
```

Script description

- analyze.py - data anylisys functions using pyparsing
- parse_memo.py - loader data into the mongo database

Folders description:
- data - collection of JSON files from lists.memo.ru (needs to be downloaded and unpacked from - )
- refined - extracted data using analyze.py
- refined2 - temp data

Data:
 - refined data as collection of CSV files - http://6342f487daa9ab45319c-2c5452fae23e39db0ab761bf51a001b6.r74.cf2.rackcdn.com/memo/memo_refined.zip
 - raw data - http://6342f487daa9ab45319c-2c5452fae23e39db0ab761bf51a001b6.r74.cf2.rackcdn.com/memo/memo_data_json.zip
 - Mongo database dump as BSON - http://6342f487daa9ab45319c-2c5452fae23e39db0ab761bf51a001b6.r74.cf2.rackcdn.com/memo/memo_data_json.zip

## Terms of use

Apache Licence 2.0