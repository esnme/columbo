import cProfile
import os
import time
from wsgiref.simple_server import make_server

from flask import Flask, render_template, send_file
import json

class Profile(object):
    def __init__(self, app):
        self.app = app
        self.profiler = cProfile.Profile()
        self.flask_app = Flask(__name__)
        self.flask_app.debug = True
        self.flask_app.root_path = os.path.dirname(os.path.abspath(__file__))

        def escape_html(html):
            return str(html).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

        @self.flask_app.route("/__profiler__")
        def index():
            return render_template('index.html')

        @self.flask_app.route("/__profiler__/stats.json")
        def stats_json():
            prof_stats = self.profiler.getstats()
            stats = []
            for s in prof_stats:
                stats.append(dict(callcount=s.callcount, reccallcount=s.reccallcount, totaltime=s.totaltime, inlinetime=s.inlinetime, code=escape_html(s.code)))
            
            return json.dumps({'stats': stats})

        # Hack to work around Flask static file serving
        @self.flask_app.route("/__profiler__/static/<filename>")
        def static_file(filename):
            return send_file("%s/static/%s" % (self.flask_app.root_path, filename))

    def __call__(self, environ, start_response):
        path_info = environ.get('PATH_INFO', '')

        if path_info.find('/__profiler__') == 0:
            return self.flask_app(environ, start_response)

        return self.profiler.runcall(self.app, environ, start_response)

def slow_function():
    time.sleep(0.05)

def simple_app(environ, start_response):
    start_response('200 OK', [('Content-type', 'text/html')])
    for i in range(1, 20):
        slowFunction()

    return ['<html><body>hej</body></html>']

if __name__ == "__main__":
    app = Profile(simple_app)
    httpd = make_server('', 8000, app)
    print "Serving on port 8000..."
    httpd.serve_forever()