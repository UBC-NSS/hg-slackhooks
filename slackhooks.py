# -*- coding: utf-8 -*-

"""
  HG changegroup hook that submits information to a slack incoming webhook
"""

import urllib2
import json

from collections import namedtuple
from mercurial.cmdutil import show_changeset


# pylint: disable=invalid-name, missing-docstring

config_group = 'slackhooks'
Config = namedtuple(
    'HgSlackHooksConfig',
    field_names=[
        'webhook_urls',
        'repo_name',
        'commit_url',
        'username',
        'icon_emoji',
        'icon_url',
    ])


def get_config(ui):
    settings = (('webhook_urls', None),
                ('repo_name', None),
                ('commit_url', None),
                ('username', None),
                ('icon_emoji', None),
                ('icon_url', None))

    tupvals = [ui.config(config_group, key, default) for key, default in settings]

    return Config(*tupvals) # pylint: disable=star-args

def pushhook(node, hooktype, url, repo, source, ui, **kwargs):
    # pylint: disable=unused-argument,too-many-arguments
    config = get_config(ui)
    username = ui.username()

    changesets = get_changesets(repo, node)
    count = len(changesets)
    messages = render_changesets(ui, repo, changesets, config)

    ensure_plural = "s" if count > 1 else ""

    if config.repo_name is not None:
        ensure_repo_name = " to \"{0}\"".format(config.repo_name) if config.repo_name else ""
    else:
        ensure_repo_name = " to \"{0}\"".format(repo.root)

    text = "{user} pushed {count} changeset{ensure_plural}{ensure_repo_name}:\n```{changes}```".format(
        user=username,
        count=count,
        ensure_plural=ensure_plural,
        ensure_repo_name=ensure_repo_name,
        changes=messages)

    post_message_to_slack(text, config)


def get_changesets(repo, node):
    node_rev = repo[node].rev()
    tip_rev = repo['tip'].rev()
    return range(tip_rev, node_rev - 1, -1)


def render_changesets(ui, repo, changesets, config):
    url = config.commit_url
    if url:
        url = url.format(repo=repo.root, rev="{node|short}")
        node_template = "<{url}|{{node|short}}>".format(url=url)
    else:
        node_template = "{node|short}"

    template = "{0}\\n".format(" | ".join([
        "{branch}",
        node_template,
        "{date(date, '%Y-%m-%d [%H:%M:%S]')}",
        "{desc|strip|firstline}",
    ]))

    displayer = show_changeset(ui, repo, {'template': template})
    ui.pushbuffer()
    for rev in changesets:
        displayer.show(repo[rev])
    return ui.popbuffer()


def post_message_to_slack(message, config):
    for target_url in config.webhook_urls.split():
        payload = {
            'text': message,
        }
        if config.username:
            payload['username'] = config.username

        payload_optional_key(payload, config, 'icon_url')
        payload_optional_key(payload, config, 'icon_emoji')
        request = urllib2.Request(target_url, "payload={0}".format(json.dumps(payload)))
        print "payload:", json.dumps(payload)
        urllib2.build_opener().open(request)

def payload_optional_key(payload, config, key):
    value = config.__getattribute__(key)
    if value:
        payload[key] = value
