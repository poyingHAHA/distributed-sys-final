import json
import os

num_of_teams = 1000

# 讀取data/login_results.json
def load_users(file_path):
    """加载用户数据"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"用户数据文件不存在: {file_path}")
    with open(file_path, "r") as file:
        return json.load(file)

# 使用login_results.json的前1000筆來生成team資料
def create_team_info(users):
    """生成團隊資料"""
    team_info = []
    for idx, user in enumerate(users[:num_of_teams]):
        team_info.append({
            "team_name": f"team_{idx+1}",
            "username": user.get("username"),
            "token": user.get("token"),
        })
    return team_info

if __name__ == "__main__":
    INPUT_FILE = "./data/login_results.json"
    try:
        users = load_users(INPUT_FILE)
        team_info = create_team_info(users)
        # 排序，依 team_name 排序
        team_info.sort(key=lambda x: x["team_name"])
        # 儲存team_info到data/team_info.json
        with open("./data/team_info.json", "w") as file:
            json.dump(team_info, file, indent=4)
    except FileNotFoundError as e:
        print(str(e))
        exit(1)
