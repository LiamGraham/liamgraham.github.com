from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # return "Index"
    return render_template('index.html')

@app.route('/blog')
def blog():
    # return "Blog"
    return render_template('blog.html')
