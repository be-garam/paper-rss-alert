import feedparser
import duckdb
from datetime import datetime
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_nature_rss(url):
    try:
        feed = feedparser.parse(url)
        return [{
            'title': entry.title,
            'publish_date': entry.published,
            'link': entry.link,
            'identifier': entry.id,
            'content': entry.content[0].value if 'content' in entry else ''
        } for entry in feed.entries]
    except Exception as e:
        logging.error(f"Error parsing Nature RSS: {str(e)}")
        return []

def parse_biorxiv_rss(url):
    try:
        feed = feedparser.parse(url)
        return [{
            'title': entry.title,
            'publish_date': entry.published,
            'link': entry.link,
            'identifier': entry.id,
            'content': entry.description
        } for entry in feed.entries]
    except Exception as e:
        logging.error(f"Error parsing bioRxiv RSS: {str(e)}")
        return []

def store_in_duckdb(data, table_name):
    try:
        conn = duckdb.connect('rss_data.db')
        conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                title VARCHAR,
                publish_date TIMESTAMP,
                link VARCHAR,
                identifier VARCHAR,
                content VARCHAR,
                update_date DATE
            )
        """)
        update_date = datetime.now().date()
        for item in data:
            conn.execute(f"""
                INSERT INTO {table_name} VALUES (?, ?, ?, ?, ?, ?)
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

if __name__ == "__main__":
    logging.info("RSS parser started")
    
    nature_url = "https://www.nature.com/nature.rss"
    biorxiv_url = "https://connect.biorxiv.org/biorxiv_xml.php?subject=all"

    nature_data = parse_nature_rss(nature_url)
    biorxiv_data = parse_biorxiv_rss(biorxiv_url)

    store_in_duckdb(nature_data, 'nature_articles')
    store_in_duckdb(biorxiv_data, 'biorxiv_articles')

    logging.info("RSS parsing and database update completed")