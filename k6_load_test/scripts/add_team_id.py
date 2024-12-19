import requests
import json

# 配置
GET_TEAMS_URL = "http://104.199.189.138:8000/api/teams/all"  # 替换为你的获取团队列表的 API 地址
TEAM_INFO_FILE = "./data/team_info.json"  # 替换为 team_info.json 的文件路径
UPDATED_TEAM_INFO_FILE = "./data/team_info.json"  # 更新后的文件路径
# TOKEN = "your_admin_or_valid_user_token"  # 替换为有权限访问 /teams/all 的 Bearer Token


def load_team_info(file_path):
    """加载 team_info.json 文件"""
    with open(file_path, "r") as file:
        return json.load(file)


def fetch_team_ids():
    """从 API 获取所有团队信息"""
    # headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.get(GET_TEAMS_URL)

    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            return {team["team_name"]: team["team_id"] for team in data.get("data", [])}
        else:
            raise Exception("Failed to fetch team data: " + data.get("message", "Unknown error"))
    else:
        raise Exception(f"Error fetching team data: {response.status_code} - {response.text}")


def update_team_info(team_info, team_ids):
    """将 team_id 添加到 team_info 中"""
    updated_team_info = []
    for team in team_info:
        team_name = team.get("team_name")
        if team_name in team_ids:
            team["team_id"] = team_ids[team_name]
        else:
            print(f"Warning: Team name '{team_name}' not found in fetched team IDs.")
        updated_team_info.append(team)
    return updated_team_info


def save_updated_team_info(file_path, updated_team_info):
    """保存更新后的 team_info.json 文件"""
    with open(file_path, "w") as file:
        json.dump(updated_team_info, file, indent=4)
    print(f"Updated team info saved to {file_path}")


def main():
    # 加载本地 team_info.json 文件
    try:
        team_info = load_team_info(TEAM_INFO_FILE)
    except FileNotFoundError:
        print(f"Error: File {TEAM_INFO_FILE} not found.")
        return

    # 从 API 获取 team_id
    try:
        team_ids = fetch_team_ids()
    except Exception as e:
        print(f"Error fetching team IDs: {e}")
        return

    # 更新 team_info 数据
    updated_team_info = update_team_info(team_info, team_ids)

    # 保存更新后的数据
    save_updated_team_info(UPDATED_TEAM_INFO_FILE, updated_team_info)


if __name__ == "__main__":
    main()
