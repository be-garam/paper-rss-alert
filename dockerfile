FROM continuumio/miniconda3

WORKDIR /app

# 시스템 패키지 및 Conda 환경 설정
RUN apt-get update && apt-get install -y cron && \
    conda create -n rss_parser python=3.9 -y && \
    echo "source activate rss_parser" > ~/.bashrc

# 환경 활성화 및 필요한 패키지 설치
COPY requirements.txt .
RUN /bin/bash -c "source activate rss_parser && pip install -r requirements.txt"

# 스크립트 복사
COPY main.py .

# Cron job 설정
RUN echo "0 14 * * * /bin/bash -c 'source activate rss_parser && python /app/main.py' >> /var/log/cron.log 2>&1" | crontab -

# 컨테이너 시작 명령
CMD ["cron", "-f"]