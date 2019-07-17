from aiohttp import web

import db
from utils import (parse_file, deserialize_json,
                   create_new_group)


async def index(request):
    return web.json_response({'Report': 'Designer'})


async def create_group(request):
    data = await request.json()
    employees = parse_file(data['file'])
    async with request.app['db_pool'].acquire() as conn:
        db_group = deserialize_json(await db.get_last_group(conn))
        # print('CALLED  create_group()')
        new_group = create_new_group(*db_group, employees)
        await db.create_data(conn, new_group)
    return web.json_response(employees)


async def get_all_groups(request):
    async with request.app['db_pool'].acquire() as conn:
        db_all_groups = deserialize_json(await db.get_all_groups(conn))
    return web.json_response(db_all_groups)


async def get_group_by_id(request):
    async with request.app['db_pool'].acquire() as conn:
        group_id = int(request.match_info['group_id'])
        try:
            group = await db.get_group_by_id(conn, group_id)
        except db.RecordNotFound as e:
            raise web.HTTPNotFound(text=str(e))

    return web.json_response(deserialize_json(group))
