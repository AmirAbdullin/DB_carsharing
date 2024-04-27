import psycopg2

conn = psycopg2.connect("""
    host=rc1d-9j70o0cpkzf8ln1s.mdb.yandexcloud.net
    port=6432
    sslmode=verify-full
    dbname=carsharing
    user=user1
    password=<пароль пользователя>
    target_session_attrs=read-write
""")

q = conn.cursor()
q.execute('SELECT version()')

print(q.fetchone())

conn.close()