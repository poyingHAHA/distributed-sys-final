import http from 'k6/http';
import { check, sleep } from 'k6';
import { SharedArray } from 'k6/data';

const test_URL = 'http://35.201.156.31:8000/api/register';
const virtual_users = 10;
// 从 JSON 文件加载用户数据
const users = new SharedArray('users', function () {
    return JSON.parse(open('../data/user_data.json')); // 修改路径为 JSON 文件的位置
});
const iter_per_vu = users.length / virtual_users;

// 配置测试选项
export const options = {
    vus: virtual_users, // 限制虚拟用户数
    iterations: users.length, // 确保所有数据被处理
    duration: '20m'
};

// 测试主函数
export default function () {
    // 确保每个 VU 处理唯一的数据条目
    const userIndex = (__VU - 1) * iter_per_vu + __ITER;
    const user = users[userIndex];

    console.log(`[VU ${__VU}] Registering user: ${userIndex}`);

    // 准备请求数据
    const payload = JSON.stringify({
        username: user.username,
        name: user.name,
        password: user.password,
    });

    const headers = { 'Content-Type': 'application/json' };

    const res = http.post(test_URL, payload, { headers });

    check(res, {
        'is status 201': (r) => r.status === 201,
        'is success true': (r) => r.json('success') === true,
        'has token': (r) => r.json('data.access_token') !== undefined,
    });

    sleep(1);
}

// K6_WEB_DASHBOARD=true K6_WEB_DASHBOARD_EXPORT=reg-v10-itr2000-d20m_register.html k6 run ./scripts/user-registration_test.js 