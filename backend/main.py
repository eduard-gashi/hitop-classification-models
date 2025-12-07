import pandas as pd
from typing import Dict
import numpy as np
from flask import Flask, jsonify
from flask_cors import CORS


from backend.processing.data_loader import load_and_process_data


app = Flask(__name__)
CORS(app)


df_metadata, pre_fb, post_fb = load_and_process_data(
    data_type="processed"
)


@app.get("/api/frageboegen")
def list_frageboegen():
    # Get list of questionnaire names
    names = [str(k) for k in pre_fb.keys() if pd.notna(k)]
    return jsonify(names)


@app.get("/api/frageboegen/<name>")
def get_fragebogen(name):
    # Get data from specific questionnaire, e.g.: "PHQ-9"
    fb = pre_fb.get(name)
    if fb is None:
        return jsonify({"error": "not found"}), 404
    print(fb.columns)
    
    # MultiIndex
    labels = [str(col[0]) for col in fb.columns]  # Questions
    codes  = [str(col[1]) for col in fb.columns]  # Codes

    flat_cols = [
        f"{col[1]}" if isinstance(col, tuple) else str(col)
        for col in fb.columns
    ]
    fb_flat = fb.copy()
    fb_flat.columns = flat_cols
    
    fb_flat = fb_flat.replace({np.nan: None})


    data = fb_flat.to_dict(orient="records")  # Get dict as rows

    return jsonify({
        "name": name,
        "labels": labels,
        "codes": codes,
        "columns": flat_cols,
        "data": data,
    })



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
