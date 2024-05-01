import redis
import os

cert_path = os.path.expanduser("~/.redis/YandexInternalRootCA.crt")

r = redis.StrictRedis(
    host="c-c9q4csipo6n7ihkil7gd.rw.mdb.yandexcloud.net",
    port=6380,
    password="R6X-ZC9-hH3-dBL",
    ssl=True,
    ssl_ca_certs=cert_path,
)

def test():
    print('test')
    r.set("foo", "bar")
    print(r.get("foo"))

if __name__ == '__main__':
    test()
