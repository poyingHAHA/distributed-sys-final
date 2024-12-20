// 創建完直接打卡
import http from 'k6/http';
import { check, sleep } from 'k6';
import { SharedArray } from 'k6/data';

const createTeamURL = 'http://35.201.156.31:8000/api/teams';
const checkinURL = 'http://35.201.156.31:8000/api/checkin';
const virtual_users = 10;

// 从 JSON 文件加载用户数据
const loginResults = new SharedArray('users', function () {
    return JSON.parse(open('../data/team_info.json')); // 修改路径为 JSON 文件的位置
});

const iter_per_vu = loginResults.length / virtual_users;

// 配置测试选项
export const options = {
    vus: virtual_users, // 限制虚拟用户数
    iterations: loginResults.length, // 确保所有数据被处理
    duration: '20m',
};

export default function () {
    if(__ITER > iter_per_vu) {
        return;
    }
    // 根据迭代数选择一个用户的 token
    const userIndex = (__VU - 1) * iter_per_vu + __ITER;
    const user = loginResults[userIndex];

    // 如果用户没有 token，跳过
    if (!user.token) {
        console.error(`User ${user.username} has no token`);
        return;
    }

    // 生成 team_name
    const teamName = user.team_name;

    // 准备创建团队请求数据
    const createPayload = JSON.stringify({
        team_name: teamName,
    });

    const headers = {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${user.token}`,
    };

    // 发送创建团队请求
    const createRes = http.post(createTeamURL, createPayload, { headers });

    // 检查团队创建是否成功
    const isTeamCreated = check(createRes, {
        'is status 201': (r) => r.status === 201,
        'team created': (r) => r.json('success') === true,
    });

    if (!isTeamCreated) {
        console.error(`Failed to create team: ${teamName}, Response: ${createRes.body}`);
        return;
    }

    // 获取新创建的 team_id
    const teamId = createRes.json('data.team_id');
    if (!teamId) {
        console.error(`Failed to retrieve team_id for team: ${teamName}`);
        return;
    }

    // 准备打卡请求数据
    const checkinPayload = JSON.stringify({
        team_id: teamId,
        post_url: 'http://aaa.com',
    });

    // 发送打卡请求
    const checkinRes = http.post(checkinURL, checkinPayload, { headers });

    // 检查打卡是否成功
    check(checkinRes, {
        'is status 200': (r) => r.status === 200,
        'checkin success': (r) => r.json('success') === true,
    });

    if (checkinRes.status !== 200) {
        console.error(`Failed to checkin for team: ${teamName}, Response: ${checkinRes.body}`);
    }

    // 模拟操作间隔
    sleep(0.5);
}

// K6_WEB_DASHBOARD=true K6_WEB_DASHBOARD_EXPORT=v10-itr1000-d20m_create_teams.html k6 run ./scripts/create_teams_test.js