# 베이스 이미지로 파이썬 3.9을 사용합니다.
FROM python:3.10

# 작업 디렉토리를 설정합니다.
WORKDIR /usr/app

# 필요한 패키지를 설치합니다.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드를 복사합니다.
COPY . .

# Uvicorn을 실행합니다.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

