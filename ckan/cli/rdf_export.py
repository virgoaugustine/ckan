# encoding: utf-8

import os
import click

from six.moves.urllib.parse import urljoin
from six.moves.urllib.error import HTTPError
from six.moves.urllib.request import urlopen

import ckan.lib.helpers as h
import ckan.logic as logic
import ckan.model as model
import ckan.plugins.toolkit as toolkit
from ckan.cli import error_shout


@click.command(
    name=u"rdf-export", short_help=u"Export active datasets as RDF.",
)
@click.argument(u"path")
@click.pass_context
def rdf_export(ctx, path):
    """ This command dumps out all currently active datasets as RDF into the
    specified folder.

    """
    if not os.path.isdir(path):
        os.makedirs(path)

    fetch_url = toolkit.config[u"ckan.site_url"]
    user = logic.get_action(u"get_site_user")(
        {u"model": model, u"ignore_auth": True}, {}
    )
    context = {
        u"model": model,
        u"session": model.Session,
        u"user": user[u"name"],
    }
    flask_app = ctx.obj.app.apps["flask_app"]._wsgi_app
    with flask_app.test_request_context():
        dataset_names = logic.get_action(u"package_list")(context, {})

        for dataset_name in dataset_names:
            dd = logic.get_action(u"package_show")(
                context, {u"id": dataset_name}
            )
            if not dd[u"state"] == u"active":
                continue

            url = h.url_for(u"dataset.read", id=dd[u"name"])

            url = urljoin(fetch_url, url[1:]) + u".rdf"
            try:
                fname = os.path.join(path, dd[u"name"]) + u".rdf"
                try:
                    r = urlopen(url).read()
                except HTTPError as e:
                    if e.code == 404:
                        return error_shout(
                            u"Please install ckanext-dcat and enable the "
                            + u"`dcat` plugin to use the RDF serializations"
                        )
                with open(fname, u"wb") as f:
                    f.write(r)
            except IOError as ioe:
                return error_shout(ioe)
