import asyncio
from databases import Database
from utils.pass_authen import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER


async def connect_db():
    db = Database(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")
    await db.connect()
    return db

#disconnect the db
async def disconnect_db(db):
    await db.disconnect()

query = "insert into books values(:isbn, :name, :author,:year)"
values = [{"isbn":'isbn1', "name":"book1", "author":"author1","year":2019},
{"isbn":'isbn2', "name":"book2", "author":"author2","year":2018}]

async def execute(query,is_many, values=None):
    db = await connect_db()
    if is_many:
        await db.execute_many(query=query, values=values)
    else:
        await db.execute(query=query, values=values)

    await disconnect_db(db)

async def fetch(query, is_one, values=None):
    db = await connect_db()

    if is_one:
        result = await db.fetch_one(query=query, values=values)
        out = dict(result)
    else:
        result = await db.fetch_all(query=query, values=values)
        out = []
        for row in result:
            out.append(dict(row))

    await disconnect_db(db)

    return out


#to run the async
loop = asyncio.get_event_loop()
loop.run_until_complete(query, False, values)