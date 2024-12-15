### 使用 DROP DATABASE 刪除資料庫
在確認沒有用戶連接該資料庫後，可以使用以下指令刪除：
```bash
DROP DATABASE your_database_name;
```
- 不能在要刪除的資料庫內執行：你需要切換到另一個資料庫（例如 postgres 或 template1），因為 PostgreSQL 不允許刪除當前使用的資料庫。
示例切換：
```bash
\c postgres
```
- 強制刪除所有連接：如果資料庫中有活躍連線，可以使用 DROP DATABASE 的強制選項（PostgreSQL 13 及更高版本支持）：
```bash
DROP DATABASE your_database_name WITH (FORCE);
```
### 重建table與匯入schema
- 執行以下 SQL 指令創建資料庫：
```bash
CREATE DATABASE your_database_name;
```
- 匯入Schema
```bash
/sql-backup$ psql -h /[public ip] -U postgres -d marketing_db -f schema.sql
```
### 刪除所有數據並重置auto increment
- 删除所有数据
使用 TRUNCATE 或 DELETE： 
```bash
DELETE FROM table_name; -- 删除所有数据

-- 重置序列，假设主键列是 `id`
ALTER SEQUENCE table_name_id_seq RESTART WITH 1;
```
