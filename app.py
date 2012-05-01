#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask,request,render_template
app = Flask(__name__)
import phigen

@app.route("/")
def gen():
    inputstr = request.values.get('input', u'プラトン')
    inputstr.encode('utf_8')
    g = phigen.Phigen()
    res = g.gen(inputstr)
    return render_template('template.html', author=inputstr, title=res['title'], contents=res['story'])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
