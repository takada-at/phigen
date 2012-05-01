#!/usr/bin/env python
# -*- coding: utf-8 -*-

import md5
import os.path
import math

def _openlist(path):
    io = open(path)
    res = []
    for line in io:
        line = line.rstrip()
        if line=='':continue
        res.append(line)
    return res

class Phigen:
    def __init__(self):
        self._prepare()
    def _prepare(self):
        datadir = os.path.join(os.path.dirname(__file__),'data')
        philosophers = _openlist(os.path.join(datadir, 'philosopher'))
        prefixes     = _openlist(os.path.join(datadir, 'prefix'))
        suffixes     = _openlist(os.path.join(datadir, 'suffix'))
        words        = _openlist(os.path.join(datadir, 'word'))
        enemies      = _openlist(os.path.join(datadir, 'enemy'))
        attacks      = _openlist(os.path.join(datadir, 'attack'))
        friends      = _openlist(os.path.join(datadir, 'friend'))
        joins        = _openlist(os.path.join(datadir, 'join'))
        config  = {}
        config['philosophers'] = philosophers
        config['prefixes']     = prefixes
        config['suffixes']     = suffixes
        config['words']        = words
        config['enemies']      = enemies
        config['attacks']      = attacks
        config['friends']      = friends
        config['joins']        = joins
        self._config = config
    def _concept(self):
        if self._rand(2)==0:
            return self._randget(self._config['words'])
        else:
            return self._randget(self._config['prefixes']) + self._randget(self._config['suffixes'])
    def _phi(self, update=False):
        if update:
            return self._config['philosophers'].pop()
        return self._randget(self._config['philosophers'])
    def _phiandcon(self):
        phi1  = self._phi()
        con1  = self._concept()
        cond  = "の" if self._rand(2)==0 else "における"
        return phi1 + cond + con1
    def _how(self):
        atype = self._rand(2)
        suffixes = ['点で', '点において', 'その姿勢において']
        suffix   = self._randget(suffixes)
        if atype==1:
            enemy = self._randget(self._config['enemies'])
            attack = self._randget(self._config['attacks'])
            base = enemy + attack
        else:
            friend = self._randget(self._config['friends'])
            join   = self._randget(self._config['joins'])
            base = friend + join
        return "%s%s" % (base, suffix)
    def _niteru(self, base0, base1=None):
        verbs = ["に似ている", "と本質的にひとしい", "と共通点がある", "と類似している", "と根底に共通するものがある"]
        verb  = self._randget(verbs)
        how   = self._how()
        if base1 is None:
            base1 = self._phiandcon()
        return "%sは%s、%s%s。" % (base0, how, base1, verb)
    def _eikyo(self, base0, base1=None):
        verbs = ["の影響がある", "の影響下にある", "を受け継ぐものである", "を徹底させたものに他ならない"]
        verb  = self._randget(verbs)
        how   = self._how()
        if base1 is None:
            base1 = self._phiandcon()
        return "%sは%s、%s%s。" % (base0, how, base1, verb)
    def _analyze(self, base0, base1=None):
        atype = self._rand(2)
        if atype == 1:
            return self._niteru(base0, base1)
        else:
            return self._eikyo(base0, base1)
    def _randget(self, l):
        return l[ self._rand(len(l)) ]
    def _rand(self, upper):
        dig = int(math.log10(upper)) + 1
        p = 0
        for i in range(dig):
            if len(self._inputnum)==0:
                self._inputnum = self._orginput[0:]
            p += int(self._inputnum.pop()) * 10 ** i
        return p % upper
    def _num(self, s):
        m = md5.new()
        m.update(s.encode('utf-8'))
        return int(m.hexdigest(), 16) & 12131231
    def genprint(self, inputstr):
        g = self.gen(inputstr)
        print g['title']
        print g['story']
    def gen(self, inputstr):
        self._prepare()
        self._inputnum = list(str(self._num(inputstr)))
        self._orginput = self._inputnum[0:]
        num = self._rand(3)
        template_id = num
        if template_id == 0:
            phi = self._phi(True)
            con = self._concept()
            title = "%sにおける%s" % (phi, con)
            story = self._analyze("%sの%s" % (phi,con))
        elif template_id == 1:
            phi0 = self._phi(True)
            phi1 = self._phi()
            con0 = self._concept()
            con1 = self._concept()
            title = "%sと%s" % (phi0, phi1)
            story = self._analyze("%sにおける%s" % (phi0,con0), "%sの%s" % (phi1, con1))
        elif template_id == 2:
            phi0 = self._phi(True)
            phi1 = self._phi()
            con0 = self._concept()
            con1 = self._concept()
            title = "%sの%sと%sの%s" % (phi0,con0,phi1,con1)
            story = self._analyze("%sにおける%s" % (phi0,con0), "%sの%s" % (phi1, con1))
        return dict(title=unicode(title, 'utf_8'),
                    story=unicode(story, 'utf_8'))

