FROM continuumio/miniconda3

WORKDIR /app

# 시스템 패키지 및 Conda 환경 설정
RUN apt-get update && apt-get install -y cron

# Conda 환경 생성 및 활성화
COPY environment.yml .
RUN conda env create -f environment.yml
RUN echo "conda activate rss_parser" >> ~/.bashrc

# 스크립트 복사
COPY main.py .

# Cron job 설정
RUN echo "0 14 * * * /bin/bash -c 'source /root/.bashrc && conda activate rss_parser && python /app/main.py' >> /var/log/cron.log 2>&1" | crontab -

# 컨테이너 시작 명령
CMD ["cron", "-f"]