import requests
import json
import os
from multiprocessing import Pool, Manager
from tqdm import tqdm  # 用于进度显示

# 配置
API_URL = "http://104.199.189.138:8000/api/token"  # 替换为你的登录 API 地址
INPUT_FILE = "./data/user_data.json"  # 用户名和密码的输入文件
OUTPUT_FILE = "./data/login_results.json"  # 登录结果输出文件
NUM_WORKERS = 8  # 进程数量
MAX_RETRIES = 4  # 最大重试次数

def load_users(file_path):
    """加载用户数据"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"用户数据文件不存在: {file_path}")
    with open(file_path, "r") as file:
        return json.load(file)

def login_user(user, retries=0):
    """执行登录请求，支持失败重试"""
    username = user.get("username")
    password = user.get("password")
    if not username or not password:
        return {
            "username": username,
            "error": "用户名或密码为空",
        }

    payload = {
        "username": username,
        "password": password,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    try:
        response = requests.post(API_URL, data=payload, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return {
                "username": username,
                "user_id": data.get("data", {}).get("user", {}).get("user_id"),
                "token": data.get("data", {}).get("access_token"),
            }
        else:
            if retries < MAX_RETRIES:
                return login_user(user, retries + 1)
            return {
                "username": username,
                "error": response.text,
            }
    except requests.RequestException as e:
        if retries < MAX_RETRIES:
            return login_user(user, retries + 1)
        return {
            "username": username,
            "error": str(e),
        }

def save_results(results, file_path):
    """将结果转换为字典格式并保存到 JSON 文件"""
    output = []
    for result in results:
        username = result.get("username")
        if username and "token" in result:
            output.append({
                "username": username,
                "user_id": result.get("user_id"),
                "token": result.get("token"),
            })
        else:
            print(f"user {username} has error: {result.get('error')}")

    sorted_users = sorted(output, key=lambda x: int(x['username'][4:]))
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as file:
        json.dump(sorted_users, file, indent=4)
    print(f"登录结果已保存到: {file_path}")

def main():
    # 加载用户数据
    try:
        users = load_users(INPUT_FILE)
    except FileNotFoundError as e:
        print(str(e))
        return

    # 使用多进程登录用户
    with Manager() as manager:
        results = manager.list()  # 用于进程间共享结果的列表

        # 使用 tqdm 显示任务进度条
        with Pool(NUM_WORKERS) as pool, tqdm(total=len(users), desc="Processing") as pbar:
            # 定义结果收集的回调函数
            def update_progress(result):
                results.append(result)
                pbar.update(1)

            # 将任务提交到进程池，并设置回调函数更新进度
            for user in users:
                pool.apply_async(login_user, args=(user,), callback=update_progress)

            pool.close()
            pool.join()

        # 保存结果
        save_results(list(results), OUTPUT_FILE)

if __name__ == "__main__":
    main()
