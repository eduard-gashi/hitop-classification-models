import pandas as pd
from typing import Dict
from flask import Flask, jsonify
from flask_cors import CORS


from backend.processing.data_loader import load_and_process_data


app = Flask(__name__)
CORS(app)

df_metadata, pre_frageboegen, post_frageboegen = load_and_process_data(
    data_type="processed"
)


@app.get("/api/frageboegen")
def list_frageboegen():
    # Keys des Dicts pre_frageboegen zurückgeben
    names = [str(k) for k in pre_frageboegen.keys() if pd.notna(k)]
    return jsonify(names)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
