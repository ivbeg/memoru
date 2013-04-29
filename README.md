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
- refined - extracted data using analyze.py
- data - collection of JSON files from lists.memo.ru



## Terms of use

Apache Licence 2.0