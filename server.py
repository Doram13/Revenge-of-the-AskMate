from flask import Flask, render_template, redirect, request
import connection
import datamanager


app = Flask(__name__)


@app.route('/')
@app.route('/list')
def index():
    return render_template(list.html)











if __name__ == "__main__":
    app.run(
      debug=True,
      port=5000
    )