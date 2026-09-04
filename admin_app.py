from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # 프론트엔드(다른 포트/도메인)에서 요청 가능하도록 허용

# ---- 최근 이벤트 상태를 메모리에 저장 ----
# 실제 서비스라면 DB에 저장해야 하지만, 지금 단계에서는 이걸로 충분합니다.
latest_events = {
    "police": None,
    "fire": None,
    "cityhall": None,
}


def make_event_record(data):
    return {
        "data": data,
        "timestamp": datetime.now().isoformat(),
    }


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Empty House Security Admin Server Running"})


# ---------------- 하드웨어 -> 서버 (신호 수신) ----------------

@app.route("/event/police", methods=["POST"])
def event_police():
    data = request.json
    latest_events["police"] = make_event_record(data)
    print("\n========== 🚓 경찰 신호 수신 ==========")
    print(latest_events["police"])
    print("=======================================\n")
    return jsonify({"message": "police event received"})


@app.route("/event/fire", methods=["POST"])
def event_fire():
    data = request.json
    latest_events["fire"] = make_event_record(data)
    print("\n========== 🚒 소방관 신호 수신 ==========")
    print(latest_events["fire"])
    print("=========================================\n")
    return jsonify({"message": "fire event received"})


@app.route("/event/cityhall", methods=["POST"])
def event_cityhall():
    data = request.json
    latest_events["cityhall"] = make_event_record(data)
    print("\n========== 🏛️ 시청 신호 수신 ==========")
    print(latest_events["cityhall"])
    print("========================================\n")
    return jsonify({"message": "cityhall event received"})


# ---------------- 서버 -> 프론트엔드 (화면에서 조회) ----------------

@app.route("/status", methods=["GET"])
def status():
    """프론트엔드가 주기적으로(예: 3~5초마다) 호출해서 최신 상태를 가져갑니다."""
    return jsonify(latest_events)


@app.route("/status/<role>", methods=["GET"])
def status_by_role(role):
    """경찰/소방/시청 화면마다 자기 role만 따로 조회하고 싶을 때"""
    if role not in latest_events:
        return jsonify({"error": "알 수 없는 role"}), 404
    return jsonify({role: latest_events[role]})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)