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

ENV PYTHONPATH=/app
CMD ["python", "app/main.py"]
