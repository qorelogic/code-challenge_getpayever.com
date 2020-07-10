# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

import flask
from flask import Flask, render_template, url_for, send_from_directory
import json as j
import os

#app = flask.Flask(__name__)
#app = flask.Flask(__name__, static_folder='/mldev/screenshots/developerLogs/screen/qore2/')
#hdir = '/mldev/work/recruiting/US/Payever/code-challenge/payever.git/src/site/business/images/'
app = flask.Flask(__name__, static_url_path='', static_folder='site/business/images')

#@app.route('/site/business/images/<path:path>')
#def send_img(path):
#    return send_from_directory('/site/business/images/', path)

@app.route('/')
def test():
    #cmd = 'ls /mldev/screenshots/developerLogs/screen/qore2/*png | perl -pe "s/.+\///g" 2> /dev/null'
    #res = os.popen(cmd).read().strip().split('\n')#[0]
    res = timestamps02()
    print res
    bu = ''
    meta = {}
    for i in res:
        meta.update({'title':i})
        meta.update({'title2':i})        
        #liquid-screenshot-qore2-1478885822.png
        #bu += '<img src="file://%s" /><br />\n' % i
        bu += '<img src="liquid-screenshot-qore2-1478885822.png" /><br />\n' #% i
        break
    #return '\n'.join(res)
    #return bu
    return render_template('developerView.html', mess=res[0:200], meta=meta)
    #return 'everything is running\n'

if __name__ == "__main__":
	app.config['DEBUG'] = False
	app.run()
