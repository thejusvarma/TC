from flask import Flask,render_template
from gen_app import app

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html')