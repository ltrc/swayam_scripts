import sys
import codecs
import re

import os
from os import listdir
from os.path import isfile, join

def striptags(data):
    p = re.compile(r'<.*?>')
    return p.sub(' ', data)

def writefile(filepath, _list):
    with open(filepath, 'w') as f:
        for item in _list:
            f.write("%s\n" % item)



inpath = sys.argv[1]
outpath_srt = inpath.replace("/","")+'out_srt'
outpath_translation = inpath.replace("/","")+'out_translation'
os.makedirs(outpath_srt, exist_ok=True)
os.makedirs(outpath_translation, exist_ok=True)


onlyfiles = [f for f in listdir(inpath) if isfile(join(inpath, f))]

for _f in onlyfiles:
    path = inpath+'/'+_f
    _list_srt = []
    _list_translation = []
    for line in codecs.open(path):
        line = line.strip()
        line = line.replace('<DOM>', '_').replace('</DOM>','_')
        line = line.replace('<equation>', '##').replace('</equation>','##')
        line = re.sub("(\<HES\>).*?(\<\/HES\>)", " ", line)
        line = re.sub("(\<HES\>).*?(\<HES\/\>)", " ", line)
        line = re.sub("(\< HES\>).*?(\<\/HES\>)", " ", line)
        line = re.sub("(HES\>).*?(\<\/HES\>)", " ", line)
        line = re.sub("(HES\>).*?(\<HES\/\>)", " ", line)
        line = " ".join(striptags(line).split())
        word_list = []
        for word in line.split():
            if word.endswith("...") or word.endswith("…"):
                pass
            else:
                word_list.append(word)
        _list_translation.append(" ".join(word_list))
        _list_srt.append(" ".join(line.split()))

    writefile(outpath_translation+'/'+_f, _list_translation)
    writefile(outpath_srt+'/'+_f, _list_srt)
