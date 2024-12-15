# Final Project Backend

## 專案概述
此專案作為一個行銷平台的後端，使用 Python 和 FastAPI 作為網頁框架。使用 Docker 進行容器化，並透過 Poetry 管理依賴套件。資料庫遷移由 Alembic 處理。

## 功能
- 使用 FastAPI 建立 API 端點。
- 使用 PostgreSQL 作為資料庫。
- 使用 Alembic 管理資料庫遷移。
- 使用 Docker 和 Docker Compose 進行容器化開發與部署。
- 使用 Poetry 管理本地開發中的依賴套件。

---

## 檔案結構
### 主要目錄：
- **`app/`**: 包含主要應用程式碼。
  - **`api/`**: 核心 FastAPI 元件，例如端點與工具。
  - **`core/`**: 配置、例外處理與安全性設定。
  - **`endpoints/`**: API 端點的實作。
  - **`migrations/`**: Alembic 的遷移腳本。
  - **`tests/`**: 單元測試與測試用的資料庫腳本。
- **`.venv/`**: 虛擬環境 (如果已建立)。

### 主要檔案：
- **`Dockerfile`**: 建立 Docker 映像檔的指令。
- **`docker-compose.yml`**: 執行多容器 Docker 應用程式的配置檔。
- **`pyproject.toml`**: Poetry 的依賴設定檔。
- **`alembic.ini`**: Alembic 的配置檔。
- **`requirements.txt`**: （選用）如果未使用 Poetry，可用於依賴管理。

---

## 安裝與設定
### 本地開發
1. **克隆專案：**
   ```bash
   git clone <repository-url>
   cd FINAL_PROJECT_BACKEND
   ```
2. **安裝 Poetry：**
   ```bash
   pip install poetry
   ```
3. **安裝依賴套件：**
   ```bash
   poetry install
   ```
4. **本地執行應用程式：**
   ```bash
   poetry run python app/main.py
   ```

### Docker 設定
1. **建立並執行 Docker 容器：**
   ```bash
   docker-compose --env-file .env up --build
   ```
2. **存取 API：**
   API 將可於 [http://localhost:8000](http://localhost:8000) 存取。

---

## 環境變數
請確保以下環境變數已設置：
- `DATABASE_URL=postgresql://user:password@db:5432/marketing_db`

在本地開發中，這些變數可以儲存在 `.env` 檔案中，並自動加載。

---

## Docker 配置
### `docker-compose.yml`
```yaml
version: "3.8"

services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/marketing_db
    depends_on:
      - db

  db:
    image: postgres:13
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=marketing_db
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

### `Dockerfile`
```dockerfile
# 使用 Python 基礎鏡像
FROM python:3.12

# 設定工作目錄
WORKDIR /app

# 安裝 Poetry
RUN pip install poetry

# 複製 Poetry 配置文件
COPY pyproject.toml poetry.lock ./

# 設置 Poetry 不創建虛擬環境
ENV POETRY_VIRTUALENVS_CREATE=false

# 安裝依賴
RUN poetry install --no-root

# 複製所有源代碼
COPY . .

# 設置 PYTHONPATH
ENV PYTHONPATH=/app

# 啟動應用程式
CMD ["python", "app/main.py"]
```


