# Тесты демонстрируют в среднем в два раза большую скорость, чем у psycopg2 (и её асинхронного варианта — aiopg
# Причина высоких показателей в том, что asyncpg реализует бинарный протокол PostgreSQL нативно, 
# без использования абстракций, вроде DB-API. Кроме того, это позволило получить простую в использовании реализацию:
# prepared statements
# scrollable cursors
# partial iteration результатов запроса
# автоматического кодирования и декодирования составных типов, массивов и их сочетания
# интуитивно понятной поддержки пользовательских типов
# pip install asyncpg
#
import asyncio
import asyncpg

async def run():
    conn = await asyncpg.connect(user='user', password='password',
                                 database='database', host='127.0.0.1')
    values = await conn.fetch('''SELECT * FROM mytable''')
    await conn.close()
    
loop = asyncio.get_event_loop()
loop.run_until_complete(run())