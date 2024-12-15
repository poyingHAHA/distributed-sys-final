# Final Project Frontend

這是一個使用 React 開發的前端專案，包含用戶認證、團隊管理、簽到系統以及排行榜功能。專案設計簡單易用，便於後續開發和維護。

## 目錄

- [功能特色](#功能特色)
- [專案結構](#專案結構)
- [安裝與使用](#安裝與使用)
- [可用腳本](#可用腳本)
- [主要依賴](#主要依賴)

---

## 功能特色

- **用戶認證系統**：提供用戶登入與註冊功能。
- **團隊管理**：新增和管理團隊資訊。
- **簽到系統**：用於追蹤用戶活動。
- **排行榜**：展示團隊排名。
- **私有路由**：使用 React Router 確保頁面安全。

---

## 專案結構

```
FINAL_PROJECT_FRONTEND/
├── node_modules/            # Node.js 相依套件
├── public/                  # 公開靜態文件夾，例如 index.html
│   └── index.html
├── src/                     # 應用程式的主要原始碼
│   ├── components/          # React 組件
│   │   ├── CheckInForm.jsx
│   │   ├── Leaderboard.jsx
│   │   ├── LoginForm.jsx
│   │   ├── Navbar.jsx
│   │   ├── PrivateRoute.jsx
│   │   ├── RegisterForm.jsx
│   │   └── TeamForm.jsx
│   ├── services/            # API 服務處理
│   │   ├── auth.js
│   │   ├── axios.js
│   │   ├── checkins.js
│   │   ├── index.js
│   │   └── team.js
│   ├── App.jsx              # 主應用程式組件
│   ├── config.js            # 設定文件
│   └── index.js             # 應用程式進入點
├── .gitignore               # Git 忽略文件
├── package-lock.json        # 套件鎖定文件
├── package.json             # 專案描述與依賴
```

---

## 安裝與使用

### 先決條件

- [Node.js](https://nodejs.org/) (建議使用 16 版以上)
- [npm](https://www.npmjs.com/) 或 [yarn](https://yarnpkg.com/)

### 安裝步驟

1. 克隆專案：
   ```bash
   git clone <repository_url>
   cd FINAL_PROJECT_FRONTEND
   ```

2. 安裝相依套件：
   ```bash
   npm install
   ```

3. 啟動開發伺服器：
   ```bash
   npm start
   ```

4. 在瀏覽器中打開 `http://localhost:3000` 來查看應用程式。

---

## 可用腳本

在專案目錄中，您可以運行以下腳本：

- **`npm start`**：在開發模式中啟動應用程式。
- **`npm build`**：構建生產環境的應用程式。
- **`npm test`**：啟動測試工具。
- **`npm eject`**：彈出配置文件（謹慎使用）。

---

## 主要依賴

以下是本專案使用的主要依賴：

- **React**：用於構建用戶界面的 JavaScript 庫。
- **React Router DOM**：React 應用程式的聲明式路由。
- **Material UI**：受歡迎的 React UI 框架。
- **Axios**：用於處理 API 請求的 Promise 為基礎的 HTTP 客戶端。
- **QS**：用於解析查詢字串的工具庫。

詳細的依賴項目請參考 `package.json` 文件。

