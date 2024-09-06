import feedparser
import duckdb
import datetime
import pytz
import logging
from typing import List, Dict

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_date(date_str: str) -> str:
    if not date_str:
        return None
    try:
        # 날짜 형식이 'YYYY-MM-DD'인지 확인
        datetime.datetime.strptime(date_str, '%Y-%m-%d')
        return date_str
    except ValueError:
        logging.warning(f"Invalid date format: {date_str}")
        return None

def parse_nature_rss(url: str) -> List[Dict]:
    try:
        feed = feedparser.parse(url)
        return [{
            'title': entry.title,
            'publish_date': parse_date(entry.get('dc_date', '')),
            'link': entry.link,
            'identifier': entry.id,
            'content': entry.content[0].value if 'content' in entry else ''
        } for entry in feed.entries]
    except Exception as e:
        logging.error(f"Error parsing Nature RSS: {str(e)}")
        return []

def parse_biorxiv_rss(url: str) -> List[Dict]:
    try:
        feed = feedparser.parse(url)
        return [{
            'title': entry.title,
            'publish_date': parse_date(entry.get('dc_date', '')),
            'link': entry.link,
            'identifier': entry.id,
            'content': entry.description
        } for entry in feed.entries]
    except Exception as e:
        logging.error(f"Error parsing bioRxiv RSS: {str(e)}")
        return []

def store_in_duckdb(data: List[Dict], table_name: str):
    try:
        conn = duckdb.connect('rss_data.db')
        conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                title VARCHAR,
                publish_date DATE,
                link VARCHAR,
                identifier VARCHAR UNIQUE,
                content VARCHAR,
                update_date DATE
            )
        """)
        update_date = datetime.datetime.now(pytz.utc).date()
        for item in data:
            conn.execute(f"""
                INSERT INTO {table_name} (title, publish_date, link, identifier, content, update_date)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT (identifier) DO UPDATE SET
                title = excluded.title,
                publish_date = excluded.publish_date,
                link = excluded.link,
                content = excluded.content,
                update_date = excluded.update_date
            """, (item['title'], item['publish_date'], item['link'], item['identifier'], item['content'], update_date))
        conn.close()
        logging.info(f"Data stored successfully in {table_name}")
    except Exception as e:
        logging.error(f"Error storing data in DuckDB: {str(e)}")

def main():
    logging.info("RSS parser started")
    
    nature_url = "https://www.nature.com/nature.rss"
    biorxiv_url = "http://connect.biorxiv.org/biorxiv_xml.php?subject=all"

    nature_data = parse_nature_rss(nature_url)
    biorxiv_data = parse_biorxiv_rss(biorxiv_url)

    store_in_duckdb(nature_data, 'nature_articles')
    store_in_duckdb(biorxiv_data, 'biorxiv_articles')

    logging.info("RSS parsing and database update completed")

if __name__ == "__main__":
    main()