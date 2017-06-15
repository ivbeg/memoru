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
 - refined data as collection of CSV files - http://cdn1.sdlabs.ru/public/datacollect/memo.ru/memo_refined.zip
 - raw data - http://cdn1.sdlabs.ru/public/datacollect/memo.ru/memo_data_json.zip
 - Mongo database dump as BSON - http://cdn1.sdlabs.ru/public/datacollect/memo.ru/memo_data_json.zip

## Terms of use

Apache Licence 2.0
