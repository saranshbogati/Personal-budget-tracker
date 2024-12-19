from fastapi import FastApi


@app.route("/")
def init():
    return "<h1>Thukka muji</h1>"
