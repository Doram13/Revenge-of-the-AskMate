from flask import Flask, render_template, redirect, request
import connection
import datamanager


app = Flask(__name__)


@app.route('/')
def index():
    return "Hello Revenge"












if __name__ == "__main__":
    app.run(
      debug=True,
      port=5000
    )