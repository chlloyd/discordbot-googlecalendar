from flask import Flask, jsonify

import googlecalendar

app = Flask(__name__)


@app.route("/next-event", methods=["POST"])
def next_event():
    contentlist = googlecalendar.getrecentevents(1)
    return jsonify(content="The next is %s on the %s at %s for %s hours in %s" % (
    contentlist[4], contentlist[0], contentlist[1], contentlist[3], contentlist[5]))


@app.route("/day-event", methods=["POST"])
def day_event():
    return None


@app.route("/next-five-events", methods=["POST"])
def next_five_event():
    contentlist = googlecalendar.getrecentevents(5)
    return jsonify(content="The next is %s on the %s at %s for %s hours in %s" % (
    contentlist[4], contentlist[0], contentlist[1], contentlist[3], contentlist[5]))

if __name__ == '__main__':
    app.run()
