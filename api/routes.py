from controllers import controller


def setup_routes(app):
    app.router.add_get('/',
                       controller.index,
                       name='index')

    app.router.add_post('/create',
                        controller.create_group,
                        name='create')

    app.router.add_get('/groups',
                       controller.get_all_groups,
                       name='all_groups')

    app.router.add_get('/groups/{group_id}',
                       controller.get_group_by_id,
                       name='group_detail')
