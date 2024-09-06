import duckdb
import os
from dotenv import load_dotenv

load_dotenv()

def view_table_content(table_name):
    db_path = os.getenv('DB_PATH', 'rss_data.db')
    conn = duckdb.connect(db_path)
    result = conn.execute(f"SELECT * FROM {table_name}").fetchall()
    conn.close()
    return result

# Nature 테이블 내용 확인
nature_content = view_table_content('nature_articles')
print("Nature Articles:")
for row in nature_content[:5]:  # 처음 5개 행만 출력
    print(row)

print("\n" + "-"*50 + "\n")

# bioRxiv 테이블 내용 확인
biorxiv_content = view_table_content('biorxiv_articles')
print("bioRxiv Articles:")
for row in biorxiv_content[:5]:  # 처음 5개 행만 출력
    print(row)