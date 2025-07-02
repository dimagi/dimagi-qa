import logging


def get_app_build_info(client, domain, app_id):
    logging.info("Entered get build info")
    response = client.get(f'/a/{domain}/cloudcare/apps/v2/?option=apps', name='build info')
    assert (response.status_code == 200)
    for app in response.json():
        if app['copy_of'] == app_id:
            return app['_id']
