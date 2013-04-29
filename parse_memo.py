# -*- coding: utf-8 -*-
import sys
import os
import os.path
import re

from lxml.html import parse
import simplejson as json
from pyparsing import Word, alphas, nums, oneOf, ParseException, lineStart, lineEnd, restOfLine, Literal, srange, Suppress
from pymongo import Connection


MIRROR_PATH = u"E:\\archive\\webdb\\memo.ru\\lists.memo.ru\\"
DATA_PATH = 'data'


def get_files(dirpath):
    return os.listdir(dirpath)


#PATTERN_F_BORN = re.compile(u'^Родилась\sв\s(?P<year>[0-9]{4,4})\s(г|году)(\.\s|\s|\.|)$')
#PATTERN_F_BORN = re.compile(r'^Родилась\s+в\s+(?P<year>[0-9]{4,4}).*$')	
PATTERN_F_BORN = lineStart + Suppress(u'Родилась') + Suppress(u'в') + Word(nums, exact=4).setResultsName(
    'year') + oneOf([u'г.', u'года']).suppress() + lineEnd
PATTERN_M_BORN = lineStart + Suppress(u'Родился') + Suppress(u'в') + Word(nums, exact=4).setResultsName('year') + oneOf(
    [u'г.', u'года']).suppress() + lineEnd
PATTERN_PRIG = lineStart + Suppress(u'Приговор:') + restOfLine.setResultsName('prigovor') + lineEnd


def parse_all():
    for p in range(1, 39, 1):
        thep = MIRROR_PATH + 'd' + str(p) + '\\'
        for fname in get_files(thep):
            frecords = []
            resname = 'data/d' + str(p) + '_' + fname.split('.')[0] + '.json'
            if os.path.exists(resname): continue
            f = open(os.path.join(thep, fname), 'r')
            lo = parse(f)
            objs = lo.xpath("//ul[@class='list-right']/li")
            for o in objs:
                record = {}
                names = o.xpath("p[@class='name']")
                if len(names) > 0:
                    namenode = names[0]
                    record['name'] = namenode.text_content()
                containers = o.xpath("p[@class='cont']")
                if containers:
                    record['text'] = containers[0].text_content()
                authors = o.xpath("p[@class='author']")
                if authors:
                    record['author'] = authors[0].text_content()
                frecords.append(record)
            results = {'records': frecords, 'filename': os.path.join(thep, fname)}
            res_file = open(resname, 'w')
            res_file.write(json.dumps(results, indent=4))
            res_file.close()
            print os.path.join(thep, fname)


def extract_sources():
    filenames = os.listdir(DATA_PATH)
    n = 0
    i = 0
    for fname in filenames:
        i += 1
        m = 0
        f = open(os.path.join(DATA_PATH, fname))
        data = json.load(f)
        f.close()
        m = len(data['records'])
        for o in data['records']:
            parts = o['author'].split(u'Источник: ')
            if len(parts) > 0:
                author = parts[1]
                print author.encode('utf8')
        n += m

#		print i, fname, m, n



def extract_text():
    filenames = os.listdir(DATA_PATH)
    n = 0
    i = 0
    for fname in filenames:
        i += 1
        m = 0
        f = open(os.path.join(DATA_PATH, fname))
        data = json.load(f)
        f.close()
        m = len(data['records'])
        for o in data['records']:
            name = o['text']
            lines = o['text'].splitlines()
            for l in lines:
                l = l.strip().replace(u'\xa0', u' ')
                if len(l) == 0: continue
                #				try:
                #					m = PATTERN_PRIG.parseString(l)
                #					print m
                #				except ParseException:
                #					pass
                print l.encode('utf8')
            print '---'

#			print name.encode('utf8')

def extract_names():
    filenames = os.listdir(DATA_PATH)
    n = 0
    i = 0
    for fname in filenames:
        i += 1
        m = 0
        f = open(os.path.join(DATA_PATH, fname))
        data = json.load(f)
        f.close()
        m = len(data['records'])
        for o in data['records']:
            name = o['name']
            print name.encode('utf8')


def load_data():
    conn = Connection()
    db = conn['memoraw']
    coll = db['records']
    collf = db['pages']
    filenames = os.listdir(DATA_PATH)
    n = 0
    i = 0
    for fname in filenames:
        i += 1
        fn = collf.find_one({'fname': fname})
        if fn is not None: continue
        m = 0
        f = open(os.path.join(DATA_PATH, fname))
        data = json.load(f)
        f.close()
        razdel, pagecode = fname.split('.', 1)[0].split('_')
        url = 'http://lists.memo.ru/%s/%s.htm' % (razdel, pagecode)
        m = len(data['records'])
        c = 0
        for o in data['records']:
            c += 1
            uniq = '%s_%s_%d' % (razdel, pagecode, c)
            r = coll.find_one({'uniqid': uniq})
            if r is not None: continue
            parts = o['author'].split(u'Источник: ')
            if len(parts) > 0:
                o['author'] = parts[1]
            o['fname'] = fname
            o['url'] = url
            o['uniqid'] = uniq
            coll.save(o)
        collf.save({'fname': fname, 'url': url, 'num': m})
        n += m
        print i, fname, m, n


if __name__ == "__main__":
#	parse_all()
#	extract_text()
#	extract_names()
    load_data()
	