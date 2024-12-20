import requests
import json
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
from time import sleep

# 配置
CREATE_TEAM_URL = 'http://35.201.156.31:8000/api/teams'
CHECKIN_URL = 'http://35.201.156.31:8000/api/checkin'
TEAM_INFO_FILE = './data/team_info.json'  # JSON 文件路径
MAX_RETRIES = 8  # 最大重试次数
NUM_OF_WORKER = 4

# 从文件加载团队信息
def load_team_info(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading team info: {e}")
        return []

# 创建团队
def create_team(team_name, token):
    payload = {
        "team_name": team_name
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(CREATE_TEAM_URL, json=payload, headers=headers)
            if response.status_code == 201:
                # print(f"Team {team_name} created successfully.")
                return response.json().get('data', {}).get('team_id')
            else:
                print(f"Failed to create team {team_name} (Attempt {attempt + 1}): {response.status_code} {response.text}")
        except Exception as e:
            print(f"Error creating team {team_name} (Attempt {attempt + 1}): {e}")

    print(f"Team {team_name} failed to be created after {MAX_RETRIES} attempts.")
    return None

# 打卡
def checkin_team(team_id, token):
    payload = {
        "team_id": team_id,
        "post_url": "http://aaa.com"
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(CHECKIN_URL, json=payload, headers=headers)
            if response.status_code == 200:
                # print(f"Checkin for team {team_id} successful.")
                return True
            else:
                print(f"Failed to checkin for team {team_id} (Attempt {attempt + 1}): {response.status_code} {response.text}")
        except Exception as e:
            print(f"Error during checkin for team {team_id} (Attempt {attempt + 1}): {e}")

    print(f"Checkin for team {team_id} failed after {MAX_RETRIES} attempts.")
    return False

# 包装创建和打卡函数以支持进度条
def process_team_with_progress(team):
    token = team.get("token")
    team_name = team.get("team_name")

    if not token:
        print(f"Skipping team {team_name}: No token provided.")
        progress_bar.update(1)
        return

    team_id = create_team(team_name, token)
    sleep(0.5)  # 等待一秒
    if team_id:
        checkin_team(team_id, token)
    sleep(0.5)  
    progress_bar.update(1)

# 主函数
def main():
    teams = load_team_info(TEAM_INFO_FILE)
    if not teams:
        print("No team info found. Exiting.")
        return

    num_workers = NUM_OF_WORKER

    global progress_bar
    with tqdm(total=len(teams), desc="Processing Teams") as progress_bar:
        with Pool(num_workers) as pool:
            pool.map(process_team_with_progress, teams)

if __name__ == "__main__":
    main()
