import http from 'k6/http';
import { check, sleep, group } from 'k6';
import { SharedArray } from 'k6/data';

let get_team_join_url = (team_id) => `http://35.201.156.31:8000/api/teams/${team_id}/join`;
let get_team_details_url = (team_id) => `http://35.201.156.31:8000/api/teams/${team_id}`;
let checkin_url = 'http://35.201.156.31:8000/api/checkin';

// 加载用户和团队数据
const loginResults = new SharedArray('loginResults', function () {
    const data = JSON.parse(open('../data/login_results.json')); // 替换为 login_results.json 的路径
    // console.log('loginResults:', Object.entries(data));
    return data
});
const teamInfo = new SharedArray('teamInfo', function () {
    return JSON.parse(open('../data/team_info.json')); // 替换为 team_info.json 的路径
});
// const virtual_users = 10;
// const iter_per_vu = loginResults.length / virtual_users;

// 配置選項
export const options = {
    // 指數增長測試
    stages: [
        { duration: '30s', target: 3 }, // 模擬 3 個用戶
        { duration: '30s', target: 9 }, // 模擬 9 個用戶
        { duration: '30s', target: 27 }, // 模擬 27 個用戶
        { duration: '30s', target: 81 },  // 模擬 81 個用戶
        { duration: '30s', target: 243 },  // 模擬 243 個用戶
        { duration: '30s', target: 729 },  // 模擬 729 個用戶
    ],
    thresholds: {
        http_req_duration: ['p(95)<2000'], // 95% 的請求時間要小於 2000ms
        'http_req_failed': ['rate<0.01'],  // 失敗率要低於 1%
    },
};

export default function () {
    // 根据迭代数选择一个用户
    const userIndex = Math.floor(Math.random() * loginResults.length);
    const user = loginResults[userIndex];
    const teamIndex = Math.floor(Math.random() * teamInfo.length);
    const team = teamInfo[teamIndex];

    // 检查用户和团队信息是否完整
    if (!user.token || !team.team_id) {
        console.error(`Invalid data: user ${user.username}, team ${team.team_name}`);
        return;
    }

    // Headers for requests
    const headers = {
        Authorization: `Bearer ${user.token}`,
        'Content-Type': 'application/json',
    };

    group(`User ${user.username} joins team ${team.team_name}`, function () {
        // Step 1: Join a team
        const joinPayload = JSON.stringify({});
        const joinRes = http.post(get_team_join_url(team.team_id), joinPayload, { headers });

        const isJoined = check(joinRes, {
            'join status is 200': (r) => r.status === 200,
            'join success': (r) => r.json('success') === true,
        });

        if (!isJoined) {
            console.error(`Failed to join team: ${team.team_name}, Response: ${joinRes.body}`);
            return;
        }

        // Simulate delay between actions
        sleep(1);

        // Step 2: Get team details to retrieve all members
        const teamDetailsRes = http.get(get_team_details_url(team.team_id), { headers });

        const isTeamDetailsFetched = check(teamDetailsRes, {
            'team details fetched': (r) => r.status === 200,
            'team members retrieved': (r) => r.json('data.members') !== undefined,
        });

        if (!isTeamDetailsFetched) {
            console.error(`Failed to fetch team details for team: ${team.team_name}, Response: ${teamDetailsRes.body}`);
            return;
        }

        // Extract team members
        const teamMembers = teamDetailsRes.json('data.members');

        // Step 3: Checkin for each member in the team
        for (const member of teamMembers) {
            console.log(member);
            // console.log(member.username.slice(4));
            // console.log(loginResults[Number(member.username.slice(4))].token);
            const memberHeaders = {
                Authorization: `Bearer ${loginResults[Number(member.username.slice(4))-1].token}`,
                'Content-Type': 'application/json',
            };

            const checkinPayload = JSON.stringify({
                team_id: team.team_id,
                post_url: 'http://aaa.com',
            });

            const checkinRes = http.post(checkin_url, checkinPayload, { headers: memberHeaders });

            check(checkinRes, {
                [`member ${member.username} checkin status is 200`]: (r) => r.status === 200,
                [`member ${member.username} checkin success`]: (r) => r.json('success') === true,
            });

            if (checkinRes.status !== 200) {
                console.error(
                    `Failed to checkin for member ${member.username} in team ${team.team_name}, Response: ${checkinRes.body}`
                );
            }

            // Simulate delay between each member's checkin
            sleep(0.5);
        }

        // Simulate delay after all members checkin
        sleep(0.5);
    });
}

// K6_WEB_DASHBOARD=true K6_WEB_DASHBOARD_EXPORT=v10-itr2000-d40m_join_and_checkin.html k6 run ./scripts/join_and_checkin_test.js 