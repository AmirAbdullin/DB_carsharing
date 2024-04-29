import asyncpg


class PG:
    def __init__(self, connection_urls):
        self.master = None
        self.urls = connection_urls
    
    async def check_master(self):
        async with self.pg_pool.acquire() as connection:
            result = await connection.fetch('''
                SHOW transaction_read_only;
                ''')
        is_master = result[0][0] == 'off'
        return is_master

    async def create_pool(self):
        db_urls = self.urls
        for db_url in db_urls:
            try:
                self.pg_pool = await asyncpg.create_pool(db_url, statement_cache_size=0)
                # Если статус transaction_read_only == 'off', значит это Master
                if await self.check_master():
                    self.master = db_url
                    return
            except Exception as ex:
                print(f'Connection to {db_url} failed: {ex}')
        self.master = None


    async def execute(self, sql, *args, **kwargs):
        if not self.master or not await self.check_master():
            await self.create_pool()
        async with self.pg_pool.acquire() as connection:
            return await connection.execute(sql, *args, **kwargs)

    
    async def executemany(self, sql, *args, **kwargs):
        if not self.master or not await self.check_master():
            await self.create_pool()
        async with self.pg_pool.acquire() as connection:
            return await connection.executemany(sql, *args, **kwargs)


    async def fetch(self, sql, *args, **kwargs):
        if not self.master or not await self.check_master():
            await self.create_pool()
        async with self.pg_pool.acquire() as connection:
            return await connection.fetch(sql, *args, **kwargs)
        

    async def get_table(self, table_name):
        table = await self.fetch(f'SELECT * FROM {table_name};')
        return table
    
    



# import psycopg2
# import os
# import traceback
# import datetime


# def exequte_query(query):
#     cur = None
#     conn = None
#     try:
#         conn = psycopg2.connect(os.environ.get("DB_REDENTIALS", ""))
#         cur = conn.cursor()
#         cur.execute(query)
#         result = cur.fetchone()
#     except Exception as ex:
#         print(ex)
#     if cur:
#         cur.close()
#     if conn:
#         conn.close()
#     return result


# def fetchall_query(query):
#     cur = None
#     conn = None
#     result = []
#     try:
#         conn = psycopg2.connect(os.environ.get("DB_CREDENTIALS", ""))
#         cur = conn.cursor()
#         cur.execute(query)
#         result = cur.fetchall()
#     except Exception as ex:
#         print(ex)

#     if cur:
#         cur.close()
#     if conn:
#         conn.close()
#     return result


# # def db_mark_review(uuid, login='', status='invalid', review=''):
# #     cur = None
# #     conn = None
# #     # print("login:", login, "status:", status, "review:", review)
# #     try:
# #         conn = psycopg2.connect(os.environ.get("DB_COMPLAINTS_CREDENTIALS", ""))
# #         cur = conn.cursor()
# #         cur.execute(f"""
# #             UPDATE
# #                 {os.environ.get("DB_COMPLAINTS_TABLE", "")}
# #             SET
# #                 status = %s,
# #                 status_set_by = %s,
# #                 review_time = %s,
# #                 review = %s
# #             WHERE
# #                 id = '{uuid}'
# #         """, (status, login, datetime.datetime.now(), review))
# #         conn.commit()
# #         print("Commited successfully:", "uuid:", uuid, "login:", login, "status:", status, "review:", review)
# #         # (id, query, answer, intro, datetime, reviewed)
# #     except Exception as ex:
# #         print(ex)
# #         print(str(traceback.format_exc()).replace('\n', '   '))

# #     if cur:
# #         cur.close()
# #     if conn:
# #         conn.close()
