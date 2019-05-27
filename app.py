from flask import Flask


app = Flask(__name__)


@app.route('/')
def calendar_webhook():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()


# https://stackoverflow.com/questions/3408097/parsing-files-ics-icalendar-using-python