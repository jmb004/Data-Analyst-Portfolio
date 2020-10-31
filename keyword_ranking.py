#!python3

"""
import modules
"""
import logging, glob, googlesearch, random, tempfile, shutil, sys, nltk, fake_useragent, wordcloud, bs4, selenium, pandas, numpy, os, selenium, openpyxl, requests, re, time, urllib.request, cert_human, pycparser, cffi, cryptography, OpenSSL, asn1crypto, certifi, ssl
from os import path
from itertools import cycle


"""
# set os
"""
cd = os.getcwd()

"""
search downloaded HTML now text files for keyword in a sentence and return the sentence with the website
"""

def keyword_search(pattern):
    pattern = re.compile(pattern)
    p = str(pattern)

    files = glob.glob("www.*.txt")

    for file in files:
        for line in open(file, encoding="utf8"):
            line = line.strip().lower()
            for match in re.finditer(pattern, line): # return an iterator of the pattern keyword and the line from the html
                try:
                    print("Found", p[12:-2], "in" , file, "here:", line) # Found (key-pattern-word) in (www.joebalog.com) here: (Joe belives in key-pattern-word).
                except:
                    raise Exception
            

# take user input
pattern = input("What is a keyword you want to search the websites for? i.e., guns") # i.e., guns

keyword_search(pattern) # run keyword search through html

