# distributed-sys-final

## 測試方法
1. 先進入k6_load_test文件夾
2. 執行`K6_WEB_DASHBOARD=true K6_WEB_DASHBOARD_EXPORT=reg-v10-itr2000-d20m_register.html k6 run ./scripts/user-registration_test.js `註冊2000個用戶
3. 執行`python ./scripts/create_team_info.py` 讓前1000個user建立team_info.json
4. 執行`K6_WEB_DASHBOARD=true K6_WEB_DASHBOARD_EXPORT=v10-itr1000-d20m_create_teams.html k6 run ./scripts/create_teams_test.js`創建1000個teams
5. 執行`python ./scripts/add_team_id.py` 幫team_info加上team_id
6. 執行`K6_WEB_DASHBOARD=true K6_WEB_DASHBOARD_EXPORT=v10-itr2000-d40m_join_and_checkin.html k6 run ./scripts/join_and_checkin_test.js`讓2000個使用者同時加入與checkin