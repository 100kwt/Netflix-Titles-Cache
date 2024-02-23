import json
import sqlite3

import redis


def get_cast():
    with sqlite3.connect(database='nt.sqlite') as connection:
        cursor = connection.cursor()

        with redis.Redis() as redis_client:
            cache_value = redis_client.get('all_cast')
            if cache_value is not None:
                return json.loads(cache_value)

            cursor.execute('SELECT title FROM netflix_titles ')
            result = cursor.fetchall()
            redis_client.set('all_cast', json.dumps(result), ex=300)

    return result


if __name__ == '__main__':
    print(get_cast())
