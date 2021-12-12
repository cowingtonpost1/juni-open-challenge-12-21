from flask import Flask, jsonify

import time
import threading
import json
import requests
import logging

config = json.load(open('config.json'))
app = Flask(__name__)

global enabled
enabled = False


def getPi(up: bool):
    if up:
        return config["PI1_IP"]
    else:
        return config["PI2_IP"]


def playNoise(up: bool):
    pi = getPi(up)
    requests.get(pi + "/play_noise/")


def dispenseTreat(up: bool):
    pi = getPi(up)
    requests.get(pi + "/dispense/")


@app.route('/detected/1/')
def detected_upstairs():
    logging.info("Detected kaya upstairs.")
    kaya_upstairs.set()
    return "OK"


@app.route('/detected/2/')
def detected_downstairs():
    logging.info("Detected kaya downstairs.")
    kaya_downstairs.set()
    return "OK"


@app.route('/reset1/')
def reset1():
    requests.get(config["PI1_IP"] + "/reset")
    return "OK"


@app.route('/reset2/')
def reset2():
    requests.get(config["PI2_IP"] + "/reset")
    return "OK"


@app.route('/enabled/', methods=['get'])
def isEnabled():
    return jsonify({"enabled": enabled})


@app.route('/disable/')
def disable():
    global enabled
    enabled = False
    return "OK"


@app.route('/enable/')
def enable():
    global enabled
    enabled = True
    playNoise(True)
    return "OK"


def noiseRepeater(up: bool):
    if up:
        while not kaya_upstairs.is_set() and enabled:
            playNoise(True)
            time.sleep(config["NOISE_INTERVAL"])
    else:
        while not kaya_downstairs.is_set() and enabled:
            playNoise(False)
            time.sleep(config["NOISE_INTERVAL"])


# Main loop
def mainLoop():
    logging.info("Starting main loop")
    up = True
    while True:
        if not enabled:
            time.sleep(10)
            kaya_upstairs.clear()
            kaya_downstairs.clear()
            continue

        if up:
            logging.info("Waiting for kaya to go upstairs.")

            kaya_upstairs.wait()
            if not enabled:
                continue

            logging.debug("Detected kaya upstairs.")

            kaya_upstairs.clear()
            kaya_downstairs.clear()

            logging.debug("Dispensing treat upstairs.  ")
            dispenseTreat(True)

            time.sleep(5)

            logging.info("Playing noise downstairs.")

            # play noise until kaya goes downstairs
            noise_thread = threading.Thread(target=noiseRepeater,
                                            args=(False, ))
            noise_thread.start()

            up = False

        if not up:
            logging.info("Waiting for kaya to go downstairs.")
            kaya_downstairs.wait()
            if not enabled:
                continue
            logging.debug("Detected kaya downstairs.")

            kaya_downstairs.clear()
            kaya_upstairs.clear()
            logging.debug("Dispensing treat downstairs")
            dispenseTreat(False)

            time.sleep(5)

            logging.info("Playing noise upstairs.")

            # play noise until kaya goes upstairs
            noise_thread = threading.Thread(target=noiseRepeater,
                                            args=(True, ))
            noise_thread.start()

            up = True


if __name__ == "__main__":
    # Setup logging
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format,
                        level=logging.INFO,
                        datefmt="%H:%M:%S",
                        filename="log.log")
    logging.level = logging.DEBUG

    # Setup kaya events
    kaya_upstairs = threading.Event()
    kaya_downstairs = threading.Event()

    # Start main loop
    thread = threading.Thread(target=mainLoop, daemon=True)
    thread.start()

    # Start web server
    app.run(port=config['PORT'], host='0.0.0.0')
