import psycopg2
import os
import traceback
import datetime


def fetch_all(query):
    cur = None
    conn = None
    # try:
    conn = psycopg2.connect(os.environ.get("DB_CREDENTIALS"))
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    # except Exception as ex:
    #     print(ex)
    if cur:
        cur.close()
    if conn:
        conn.close()
    return result