# app.py

# 필요한 라이브러리들을 불러옵니다.
from flask import Flask, render_template, jsonify
import random

# Flask 웹 애플리케이션을 생성합니다.
app = Flask(__name__)

# --- 초기 데이터 설정 ---
# 실제로는 데이터베이스에서 가져오겠지만, 여기서는 간단하게 리스트로 만듭니다.
robots = [
    {"id": "robot_01", "name": "로봇 알파", "lat": 37.5665, "lng": 126.9780},
    {"id": "robot_02", "name": "로봇 베타", "lat": 37.5651, "lng": 126.9770},
    {"id": "robot_03", "name": "로봇 감마", "lat": 37.5658, "lng": 126.9792}
]

# --- 라우팅(Routing) 설정: 특정 주소로 요청이 오면 어떤 함수를 실행할지 정합니다. ---

# 1. 메인 페이지를 보여주는 역할
@app.route('/')
def index():
    """
    사용자가 웹 브라우저에서 'http://127.0.0.1:5000/' 주소로 접속하면
    이 함수가 실행됩니다.
    'templates' 폴더 안에 있는 'index.html' 파일을 찾아서 사용자에게 보내줍니다.
    """
    return render_template('index.html')

# 2. 로봇 데이터를 보내주는 역할 (API)
@app.route('/robots')
def get_robots():
    """
    웹 페이지의 자바스크립트가 'http://127.0.0.1:5000/robots' 주소로 데이터를 요청하면
    이 함수가 실행됩니다.
    기존 로봇 데이터에 실시간 센서 값(온도, 습도)을 임의로 추가하여
    JSON 형식으로 변환한 후 응답으로 보내줍니다.
    """
    robots_with_sensor_data = []
    for robot in robots:
        # 기존 로봇 정보 복사
        updated_robot = robot.copy()
        
        # 랜덤 센서 데이터 추가
        updated_robot['temperature'] = round(random.uniform(20.0, 35.0), 1) # 20.0 ~ 35.0 사이의 소수 첫째자리까지
        updated_robot['humidity'] = random.randint(40, 60) # 40 ~ 60 사이의 정수
        
        # 고장 상태 랜덤으로 추가 (10% 확률로 True)
        updated_robot['is_error'] = random.random() < 0.1
        
        robots_with_sensor_data.append(updated_robot)

    # 파이썬 리스트/딕셔너리를 JSON 데이터 형태로 변환하여 반환
    return jsonify(robots_with_sensor_data)

# --- 웹 서버 실행 ---
if __name__ == '__main__':
    """
    이 파이썬 파일을 직접 실행했을 때만 웹 서버를 구동합니다.
    debug=True 옵션은 코드를 수정할 때마다 서버를 자동으로 재시작해줘서 개발 시 편리합니다.
    """
    app.run(debug=True)