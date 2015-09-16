# -*- code:utf-8 -*-
from flask import Flask, render_template
from livereload import Server

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html',
                           title="<h1>Hello world</h1>",
                           body="## Header2")

@app.template_filter('md')
def markdown_to_html(txt):
    from markdown import markdown
    return markdown(txt)

def read_md(filename):
    with open(filename) as md_file:
        content = reduce(lambda x, y: x + y, md_file.readlines())
    return content.decode('utf-8')



@app.context_processor
def inject_methods():
    return dict(read_md=read_md)

if __name__ == '__main__':
    live_server = Server(app.wsgi_app)
    live_server.watch('**/*.*')
    live_server.serve(open_url=True)
