import requests
import json
from multiprocessing import Pool, cpu_count
from tqdm import tqdm

# 配置
TEST_URL = 'http://104.199.189.138:8000/api/register'
USER_DATA_FILE = './data/user_data.json'  # JSON 文件路径
MAX_RETRIES = 5
NUM_OF_WORKER = 4

# 从文件加载用户数据
def load_user_data(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading user data: {e}")
        return []

# 注册用户
def register_user(user):
    payload = {
        "username": user["username"],
        "name": user["name"],
        "password": user["password"]
    }
    headers = {'Content-Type': 'application/json'}

    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(TEST_URL, json=payload, headers=headers)
            if response.status_code == 201:
                # print(f"User {user['username']} registered successfully.")
                # print("Access Token:", response.json().get('data', {}).get('access_token'))
                return True
            else:
                print(f"Failed to register user {user['username']} (Attempt {attempt + 1}): {response.status_code} {response.text}")
        except Exception as e:
            print(f"Error registering user {user['username']} (Attempt {attempt + 1}): {e}")

    print(f"User {user['username']} failed to register after {MAX_RETRIES} attempts.")
    return False

# 包装注册用户函数以支持进度条
def register_user_with_progress(user):
    success = register_user(user)
    if not success:
        print(f"Retrying user {user['username']}...")
    progress_bar.update(1)

# 主函数
def main():
    users = load_user_data(USER_DATA_FILE)
    if not users:
        print("No user data found. Exiting.")
        return

    # 使用多进程池进行并行处理，并添加进度条
    num_workers = NUM_OF_WORKER
    global progress_bar
    with tqdm(total=len(users), desc="Registering Users") as progress_bar:
        with Pool(num_workers) as pool:
            pool.map(register_user_with_progress, users)

if __name__ == "__main__":
    main()
