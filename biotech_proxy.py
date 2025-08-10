from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/api/trials", methods=["GET"])
def get_trials():
    # Read query params from GPT call
    phase = request.args.get("phase", "Phase 3")
    days_ahead = int(request.args.get("days_ahead", 180))
    max_results = int(request.args.get("max_results", 50))

    # Build ClinicalTrials.gov API URL
    fields = "NCTId,Condition,Phase,BriefTitle,LeadSponsorName,PrimaryCompletionDate,OverallStatus"
    base_url = "https://clinicaltrials.gov/api/query/study_fields"

    params = {
        "expr": f'AREA[Phase]{phase}',
        "fields": fields,
        "min_rnk": 1,
        "max_rnk": max_results,
        "fmt": "json"
    }

    try:
        r = requests.get(base_url, params=params, headers={"User-Agent": "BiotechRadarProxy/1.0"})
        r.raise_for_status()
        data = r.json()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
