#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask,request,render_template,url_for
import urllib
app = Flask(__name__)
import phigen

@app.route("/")
def gen():
    inputstr = request.values.get('input', u'プラトン')
    g = phigen.Phigen()
    res = g.gen(inputstr)
    url = "http://vivid-mist-6790.herokuapp.com?input=" + urllib.quote(inputstr.encode('utf-8'))
    summary = u"#哲学論文ジェネレーター 著者: %s タイトル：%s 要約: %s %s" %(inputstr, res['title'], res['story'], url)
    twitter = 'http://twitter.com/home?status=%s' % urllib.quote(summary.encode('utf-8'))
    return render_template('template.html', author=inputstr, title=res['title'], contents=res['story'], twitter=twitter)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
