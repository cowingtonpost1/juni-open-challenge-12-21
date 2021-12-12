from flask import Flask
from os.path import exists as file_exists
import logging
import json
from pydub import AudioSegment
from pydub.playback import play as play_sound
import motor

app = Flask(__name__)
config = json.load(open("config.json"))
treat_file = config["treat_state_filename"]
global treats_remaining
treats_remaining = 0


@app.route("/dispense/")
def dispense():
    global treats_remaining
    if (treats_remaining == 0):
        logging.info("no treats remaining")
        return

    # get angle to turn the servo to
    servo_states = config["servo_states"]
    angle = servo_states[str(config["max_treats"] - treats_remaining + 1)]

    # subtract 1 from the treats remaining
    treats_remaining -= 1
    motor.SetAngle(angle)
    return "OK"


@app.route("/reset")
def reset():
    global treats_remaining
    logging.info("treats reset")
    treats_remaining = config["max_treats"]
    motor.SetAngle(0)
    return "OK"


@app.route("/play_noise/")
def play_noise():
    noise = AudioSegment.from_wav(config["noise_file"])
    play_sound(noise)
    logging.info("playing noise")
    return "OK"


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    # get amount of treats remaining from file
    treats_file = config["treat_state_filename"]
    if file_exists(treat_file):
        with open(treats_file) as f:
            treats_remaining = int(f.readline())
    else:
        treats_remaining = config["max_treats"]
    try:
        # start web server
        app.run(host="0.0.0.0")
    finally:
        with open(treats_file, "w") as f:
            f.write(str(treats_remaining))
