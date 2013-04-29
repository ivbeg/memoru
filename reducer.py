#!/usr/bin/python
# -*- coding: utf-8 -*-
# TODO: This script used to custom map/reduce processing. Basic functions should be kept evertithing else moved to the toolkit

# This is reducer.py script. It accepts n-gram stats file and returns adopted map

import sys, os, re


def reduce_lines():	
	"""Reduces as lines"""
	keys = {}
	i = 0
	for line in sys.stdin:    
		i += 1
		line = line.strip()
		key = line
		v = keys.get(line, 0)
		keys[line] = v + 1
	thedict = sorted(keys.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
	for key, val in thedict:
		print '%s\t%d' %(key, val)

def reduce_to_values():
    """Reduces n-grams by dividing n-gram values by minimal value of character"""
    keys = {}
    i = 0
    for line in sys.stdin:    
	i += 1
	if i % 500 == 0:
	    print 'Processed %d' %(i)
	line = line.strip()
	m = 4000
	(word, val) = line.split('\t', 1)
	val = int(val)
	word = word.decode('utf8')
	for ch in word:
	    m = min(ord(ch), m)
	arr = []
	for ch in word:
	    arr.append(ord(ch) - m)
	key = '_'.join(map(str, arr))
	if key not in keys.keys():
	    keys[key] = val
	else:
	    keys[key] += val

    thedict = sorted(keys.items(), lambda x, y: cmp(x[1], y[1]), reverse=False)
    for key, val in thedict:
	print '%s\t%d' %(key, val)
    pass


def reduce_to_int():
    """Reduces n-grams by summ of values"""
    keys = {}
    for line in sys.stdin:    
	line = line.strip()
	m = 4000
	(word, val) = line.split('\t', 1)
	val = int(val)
	word = word.decode('utf8')
#	for ch in word:
#	    m = min(ord(ch), m)
	key = 0
	for ch in word:
	    key += ord(ch)
#	key = key / len(word)
	if key not in keys.keys():
	    keys[key] = val
	else:
	    keys[key] += val

    thedict = sorted(keys.items(), lambda x, y: cmp(x[1], y[1]), reverse=False)
    for key, val in thedict:
	print '%s\t%d' %(key, val)
    pass

def reduce_to_diff():
    """Reduces n-grams by sum of difference of values"""
    keys = {}
    for line in sys.stdin:    
	line = line.strip()
	m = 4000
	(word, val) = line.split('\t', 1)
	val = int(val)
	word = word.decode('utf8')
	for ch in word:
	    m = min(ord(ch), m)
	key = 0
	arr = []
	for ch in word:
	    key += ord(ch) - m
#	    arr.append(ord(ch) - m)
#	for 	    
#	key = key / len(word)
	if key not in keys.keys():
	    keys[key] = val
	else:
	    keys[key] += val

    thedict = sorted(keys.items(), lambda x, y: cmp(x[1], y[1]), reverse=False)
    for key, val in thedict:
	print '%s\t%d' %(key, val)
    pass


def reduce_to_smartdiff():
    """Reduces n-grams by summ of values"""
    keys = {}
    for line in sys.stdin:    
	line = line.strip()
	m = 4000
	(word, val) = line.split('\t', 1)
	val = int(val)
	word = word.decode('utf8')
	for ch in word:
	    m = min(ord(ch), m)
	key = 0
	arr = []
	for ch in word:
	    arr.append(ord(ch))# - m)
#	    key += ord(ch) - m
	if len(arr) == 4:
	    m1 = abs(arr[0] - arr[3])
	    m2 = abs(arr[1] - arr[3])
#	    key = m1 * m2
#	print key
#	for 	    
#	key = key / len(word)
	if key not in keys.keys():
	    keys[key] = val
	else:
	    keys[key] += val

    thedict = sorted(keys.items(), lambda x, y: cmp(x[1], y[1]), reverse=False)
    for key, val in thedict:
	print '%s\t%d' %(key, val)
    pass



if __name__ == "__main__":
#    reduce_to_values()
#    reduce_to_int()
#    reduce_to_diff()
#    reduce_to_smartdiff()
	reduce_lines()
