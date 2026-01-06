"""
Flask server for Emotion Detection application.

Routes:
- / : renders templates/index.html
- /emotionDetector : returns formatted emotion analysis output
"""

from flask import Flask, render_template, request

from EmotionDetection import emotion_detector

INVALID_TEXT_MESSAGE = "Invalid text! Please try again!"

app = Flask(__name__)


@app.route("/")
def home():
    """Render the home page."""
    return render_template("index.html")


@app.route("/emotionDetector", methods=["GET", "POST"])
def emotion_detector_endpoint():
    """Run emotion detection and return a user-friendly response string."""
    text_to_analyze = request.args.get("textToAnalyze")
    if text_to_analyze is None:
        text_to_analyze = request.form.get("textToAnalyze")

    if not text_to_analyze or not text_to_analyze.strip():
        return INVALID_TEXT_MESSAGE

    result = emotion_detector(text_to_analyze)

    if not isinstance(result, dict) or result.get("dominant_emotion") is None:
        return INVALID_TEXT_MESSAGE

    anger = result["anger"]
    disgust = result["disgust"]
    fear = result["fear"]
    joy = result["joy"]
    sadness = result["sadness"]
    dominant = result["dominant_emotion"]

    return (
        "For the given statement, the system response is "
        f"'anger': {anger}, 'disgust': {disgust}, 'fear': {fear}, 'joy': {joy} "
        f"and 'sadness': {sadness}. The dominant emotion is {dominant}."
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    