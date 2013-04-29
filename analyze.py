# -*- coding: utf-8 -*-
import sys, os, os.path, re
from lxml.html import parse
import simplejson as json
from pyparsing import Word, alphas, nums, oneOf, ParseException, lineStart, lineEnd, restOfLine, Literal, srange, Suppress, SkipTo, OneOrMore, printables, alphanums, alphas8bit

from pymongo import Connection

MIRROR_PATH = u"E:\\archive\\webdb\\memo.ru\\lists.memo.ru\\"
DATA_PATH = 'data'

def get_files(dirpath):
	return os.listdir(dirpath)

extended_chars = srange(r"[\0x80-\0x7FF]")
special_chars = ' -'''
allchars = alphanums + alphas8bit + extended_chars + special_chars

# Prepare months
RUS_MONTH_NAMES = [u'января', u'февраля', u'марта', u'апреля', u'мая', u'июня', u'июля', u'августа', u'сентября', u'октября', u'ноября', u'декабря']
RUS_MONTH_MAP = {}
i = 0
for k in RUS_MONTH_NAMES:
	i += 1
	RUS_MONTH_MAP[k] = i

PAT_YEAR = lineStart + Suppress(u'в') + Word(nums, exact=4).setResultsName('year') + oneOf([u'г.', u'года']).suppress() + lineEnd
PAT_RUDATE = lineStart + Word(nums, min=1, max=2).setResultsName('day') + oneOf(RUS_MONTH_NAMES).setResultsName('month_r') + Word(nums, exact=4).setResultsName('year') + oneOf([u'г.', u'года']).suppress() + lineEnd
PAT_RUDATE_WHO = lineStart + OneOrMore(Word(allchars)).setResultsName('who') + Word(nums, min=1, max=2).setResultsName('day') + oneOf(RUS_MONTH_NAMES).setResultsName('month_r') + Word(nums, exact=4).setResultsName('year') + oneOf([u'г.', u'года']).suppress() + lineEnd

PAT_OBV = lineStart + Suppress(u', обв.:') + restOfLine.setResultsName('restof') + lineEnd
PAT_OBV_YEAR = lineStart + Suppress(u'в') + Word(nums, exact=4).setResultsName('year') + oneOf([u'г.', u'года']).suppress() + Suppress(u', обв.:') + restOfLine.setResultsName('restof') + lineEnd
PAT_OBV_RUDATE = lineStart + Word(nums, min=1, max=2).setResultsName('day') + oneOf(RUS_MONTH_NAMES).setResultsName('month_r') + Word(nums, exact=4).setResultsName('year') + oneOf([u'г.', u'года']).suppress() + Suppress(u', обв.:') + restOfLine.setResultsName('restof') + lineEnd

PAT_OBV_WHO = lineStart + OneOrMore(Word(allchars)).setResultsName('who') + Word(nums, min=1, max=2).setResultsName('day') + oneOf(RUS_MONTH_NAMES).setResultsName('month_r') + Word(nums, exact=4).setResultsName('year') + oneOf([u'г.', u'года']).suppress() + Suppress(u', обв.:') + restOfLine.setResultsName('restof') + lineEnd


PAT_BORN_P = lineStart + Suppress(u'в') + Word(nums, exact=4).setResultsName('year') + oneOf([u'г.', u'года']).suppress() +  Suppress(u',') + restOfLine.setResultsName('restof') + lineEnd

#PATTERN_F_BORN = re.compile(u'^Родилась\sв\s(?P<year>[0-9]{4,4})\s(г|году)(\.\s|\s|\.|)$')	
#PATTERN_F_BORN = re.compile(r'^Родилась\s+в\s+(?P<year>[0-9]{4,4}).*$')	
#PATTERN_F_BORN = lineStart + Suppress(u'Родилась') + Suppress(u'в') + Word(nums, exact=4).setResultsName('year') + oneOf([u'г.', u'года']).suppress() + lineEnd
#PATTERN_M_BORN = lineStart + Suppress(u'Родился') + Suppress(u'в') + Word(nums, exact=4).setResultsName('year') + oneOf([u'г.', u'года']).suppress() + lineEnd
PATTERN_PRIG = lineStart + Suppress(u'Приговор:') + restOfLine.setResultsName('restof') + lineEnd
PATTERN_FBORN = lineStart + Suppress(u'Родилась') + restOfLine.setResultsName('restof') + lineEnd
PATTERN_MBORN = lineStart + Suppress(u'Родился') + restOfLine.setResultsName('restof') + lineEnd
PATTERN_SHBORN = lineStart + Suppress(u'Род. ') + restOfLine.setResultsName('restof') + lineEnd
PATTERN_FHABIT = lineStart + Suppress(u'Проживала:') + restOfLine.setResultsName('restof') + lineEnd
PATTERN_MHABIT = lineStart + Suppress(u'Проживал:') + restOfLine.setResultsName('restof') + lineEnd
PATTERN_SHHABIT = lineStart + Suppress(u'Прож.:') + restOfLine.setResultsName('restof') + lineEnd
PATTERN_FREAB = lineStart + Suppress(u'Реабилитирована ') + restOfLine.setResultsName('restof') + lineEnd
PATTERN_MREAB = lineStart + Suppress(u'Реабилитирован ') + restOfLine.setResultsName('restof') + lineEnd
PATTERN_FHPRIG = lineStart + Suppress(u'Приговорена:') + restOfLine.setResultsName('restof') + lineEnd
PATTERN_MHPRIG = lineStart + Suppress(u'Приговорен:') + restOfLine.setResultsName('restof') + lineEnd
PATTERN_FARREST = lineStart + Suppress(u'Арестована ') + restOfLine.setResultsName('restof') + lineEnd
PATTERN_MARREST = lineStart + Suppress(u'Арестован ') + restOfLine.setResultsName('restof') + lineEnd
PATTERN_SHARREST = lineStart + Suppress(u'Арест. ') + restOfLine.setResultsName('restof') + lineEnd
PATTERN_FRASSTREL = lineStart + Suppress(u'Расстреляна ') + restOfLine.setResultsName('restof') + lineEnd
PATTERN_MRASSTREL = lineStart + Suppress(u'Расстрелян ') + restOfLine.setResultsName('restof') + lineEnd
PATTERN_DEATHPLACE = lineStart + Suppress(u'Место захоронения - ') + restOfLine.setResultsName('restof') + lineEnd

PATTERN_MAP = [(PATTERN_PRIG , 'prigovor', None), 
	(PATTERN_SHBORN , 'born', None),
	(PATTERN_FBORN , 'born', 'f'), 
	(PATTERN_MBORN , 'born', 'm'),
	(PATTERN_FHABIT, 'habit', 'f'),
	(PATTERN_MHABIT, 'habit', 'm'),
	(PATTERN_SHHABIT, 'habit', None),
	(PATTERN_FREAB, 'reab', 'f'),
	(PATTERN_MREAB, 'reab', 'm'),
	(PATTERN_FHPRIG, 'whoprig', 'f'),
	(PATTERN_MHPRIG, 'whoprig', 'm'),
	(PATTERN_FARREST, 'arrest', 'f'),
	(PATTERN_MARREST, 'arrest', 'm'),
	(PATTERN_SHARREST, 'arrest', None),
	(PATTERN_FRASSTREL, 'rasstrel', 'f'),
	(PATTERN_MRASSTREL, 'rasstrel', 'm'),
	(PATTERN_DEATHPLACE, 'deathplace', None),
]

LINE_TYPES = ['prigovor', 'born', 'reab', 'habit', 'whoprig', 'arrest', 'rasstrel', 'deathplace', 'unk']

PATTERNS = {'year' : {'pat' : PAT_YEAR},
	'rudate' : {'pat' : PAT_RUDATE}
}


class MemoProcessor:
	def __init__(self):
		self.conn = Connection()
		self.db = self.conn['memoraw']
		self.coll = self.db['records']
		self.dbp = self.conn['memo']
		self.collp = self.dbp['records']
		self.load_bornkeys()

	def load_bornkeys(self):
		self.bornkeys = {}
		f = open('refined/born_vkeys.csv')
		n = 0
		for l in f:
			parts = l.decode('utf8').split(u'\t')
			if len(parts) > 2 and len(parts[2].strip()) > 0:
				self.bornkeys[parts[0]] = 1
				n += 1

	def convert_records(self):
		"""Parses all records and split text to lines. Classifies each line and transfers records to other db"""
		cn = 0
		for o in self.coll.find():
			cn += 1
			if cn % 1000 == 0: print cn
			name = o['text']
			lines = o['text'].splitlines()
			o['lines'] = []
			n = 0
			for l in lines:
				n += 1
				l = l.strip().replace(u'\xa0', u' ')
				if len(l) == 0: 
					continue
				found = False
				for p, ltype, gender in PATTERN_MAP:
					try:
						m = p.parseString(l)
						restof = m['restof'].strip()
						o['lines'].append({'n' : n, 'len' : len(restof), 'ltype' : ltype, 'text' : restof})
						if gender is not None and not o.has_key('gender'):
							o['gender'] = gender
						found = True
						break
					except ParseException:
						continue
				if not found:
					o['lines'].append({'n' : n, 'len' : len(l), 'ltype' : 'unk', 'text' : l})
			del o['text']
			del o['lproc']
			self.collp.save(o)

	def process_text(self):
		"""Parses all records and split text to lines. Classifies each line"""
#		print self.coll.find({'lproc': {'$exists' : False}}).count()
		print self.coll.find({'lines.unk': {'$exists' : False}}).count()
		cn = 0
		for o in self.coll.find({'lines.unk': {'$exists' : False}}):
			cn += 1
			if cn % 1000 == 0: print cn
			name = o['text']
			lines = o['text'].splitlines()
			o['lines'] = []
			n = 0
			for l in lines:
				n += 1
				l = l.strip().replace(u'\xa0', u' ')
				if len(l) == 0: 
#					o['lines'].append({'n' : n, 'len' : len(l), 'ltype' : 'blank', 'text' : l})
					continue
				found = False
				for p, ltype, gender in PATTERN_MAP:
					try:
						m = p.parseString(l)
						restof = m['restof'].strip()
						o['lines'].append({'n' : n, 'len' : len(restof), 'ltype' : ltype, 'text' : restof})
						if gender is not None:
							o['gender'] = gender
						found = True
						break
					except ParseException:
						continue
				if not found:
					o['lines'].append({'n' : n, 'len' : len(l), 'ltype' : 'unk', 'text' : l})
			o['lproc'] = True
			self.coll.save(o)

	def mark_record(self, line):
		whoprig_pats = [PAT_OBV, PAT_OBV_YEAR, PAT_OBV_RUDATE]
		born_pats = [PAT_BORN_P]
		if line['ltype'] in ['born', 'reab', 'rasstrel', 'whoprig', 'arrest']:
			for k in PATTERNS.keys():
				try:
					p = PATTERNS[k]['pat']
					m = p.parseString(line['text'])
					return True
				except ParseException:
					continue
		if line['ltype'] == 'whoprig':
			for p in whoprig_pats:				
				try:
					r = p.parseString(line['text'])
					return True
				except ParseException, e:
					continue
		if line['ltype'] == 'born':
			try:
				m = PAT_BORN_P.parseString(line['text'])
				restof = m['restof']
				values = restof.split(';')
				found = True
				for v in values:
					v = v.strip()
					if len(v) > 0:
						kv = self.bornkeys.get(v, None)
						if kv is None: found = False
				if found is True: 
#					print restof.encode('cp866')
					return True				
			except:
				pass		
		elif line['ltype'] == 'unk' and line['n'] == 1 and len(line['text']) > 0:
			if line['text'][0] == '(' and line['text'][-1] == ')':
				return True
		return False
				

	def calc_stats(self):
		fkeys = LINE_TYPES
		files = {}
		for k in fkeys:
			files[k] = open('refined2/%s.csv' %(k), 'w')
		stats = {}
		for lt in LINE_TYPES:		
			stats[lt] = {'num' : 0, 'proc' : 0}
		n = 0
		n_p = 0
		for o in self.collp.find():
			n += 1
			st = {}
			parsed = True
			for l in o['lines']:
				st[l['ltype']] = {'num' : 1, 'proc' : 0}
				if self.mark_record(l):
					st[l['ltype']]['proc'] = 1
				else: 
					if l['ltype'] not in ['prigovor', 'habit', 'deathplace']: 
						parsed = False
						try:
							s = u'%s\n' %(l['text'])
						except:
							continue				
						files[l['ltype']].write(s.encode('utf8'))
			if parsed: n_p += 1
			for k, v in st.items():
				stats[k]['num'] += v['num']
				stats[k]['proc'] += v['proc']
			if n % 1000 == 0:
				print 'n = %d (parsed = %d, %d%%)' %(n, n_p, 100.0 * n_p / n)
				for k, v in stats.items():
					sh = 100.0 * v['proc'] / v['num'] if v['num'] > 0 else 0
					print '- %s : %d (identified %d, %d%%)' %(k, v['num'], v['proc'], sh)

	def dump_by_ltype(self):
		fkeys = LINE_TYPES
		files = {}
		for k in fkeys:
			files[k] = open('refined/%s.csv' %(k), 'w')
		n = 0
		for o in self.collp.find():
			n += 1
			for l in o['lines']:
				if l['ltype'] not in fkeys: continue
				try:
#					s = u'%s|%s|%d|%s\n' %(o['uniqid'], o['name'], l['n'], l['text'])
					s = u'%s\n' %(l['text'])
				except:
					continue				
				files[l['ltype']].write(s.encode('utf8'))
			if n % 5000 == 0:
				print 'processed %d' %(n)
		
	def refine_whoprig(self):
		"""Refines data from prigovor"""
		pats = [PAT_OBV, PAT_OBV_YEAR, PAT_OBV_RUDATE, PAT_RUDATE_WHO, PAT_OBV_WHO]
		f = open('refined/whoprig.csv', 'r')
		for l in f:
			l = l.strip().decode('utf8')
#			print l
			found  = False
			restof = None
			for p in pats:				
				try:
					r = p.parseString(l)
					found = True
					restof = r['restof'].strip()
					print restof.encode('utf8')
					break
				except ParseException, e:
					continue

	def refine_born(self):
		"""Refines data from born"""
		pats = [PAT_BORN_P,]
		f = open('refined/born.csv', 'r')
		for l in f:
			l = l.strip().decode('utf8')
#			print l
			found  = False
			restof = None
			for p in pats:				
				try:
					r = p.parseString(l)
					found = True
					restof = r['restof'].strip()
					values = restof.split(';')
					val2 = values[0].split(',')
					for v in val2:
						v = v.strip()
						if len(v) > 0: print v.encode('utf8')					
#					if len(values) == 1: continue
#					for v in values[1:]:
#						v = v.strip()
#						if len(v) > 0: print v.encode('utf8')
					break
				except ParseException, e:
					continue
			
				
			
			
		

	def run_cmd(self, s):
		f = getattr(self, s)
		f()
				
		


if __name__ == "__main__":
	processor = MemoProcessor()
	processor.run_cmd(sys.argv[1])
#	processor.convert_records()
#	processor.process_text()
#	processor.dump_by_ltype()
#	processor.calc_stats()
	