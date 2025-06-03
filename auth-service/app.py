from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/auth/ping')
def ping():
    return jsonify({"message": "Auth service is alive!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)