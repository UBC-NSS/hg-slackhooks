# -*- coding: utf-8 -*-

"""
  HG changegroup hook that submits information to a slack incoming webhook
"""

import urllib2
import json
import os

from collections import namedtuple
from mercurial import util
from mercurial.i18n import _
from mercurial.cmdutil import show_changeset


# pylint: disable=invalid-name, missing-docstring

Defaults = (
    ('webhook_urls', None),  # List of Slack POST URLs
    ('repo_name', None),     # Optional config-hardcoded name for the repo.
    ('web_strip', 0),        # Optional num leading slashes to remove from abs path of a repo to form web path
    ('commit_url', None),    # Optional templated URL to view diff
    ('username', None),      # Optional username to use as the source of a message
    ('icon_emoji', None),    # Optional emoji to display next to the message on Slack
    ('icon_url', None))      # Optional instead of an emoji, display that url as the sender on Slack

config_group = 'slackhooks'
Config = namedtuple(
    'HgSlackHooksConfig',
    field_names=[default[0] for default in Defaults])

def web_path(path, config):
    '''strip leading slashes from local path, turn into web-safe path.'''
    path = util.pconvert(path)
    count = config.web_strip
    while count > 0:
        c = path.find('/')
        if c == -1:
            break
        path = path[c+1:]
        count -= 1
    return path

def get_config(ui):
    def _parse_setting(key, defval):
        if isinstance(defval, bool):
            val = ui.configbool(config_group, key, defval)
        elif isinstance(defval, int):
            val = int(ui.config(config_group, key, defval))
        else:
            val = ui.config(config_group, key, defval)
        return val

    tupvals = [_parse_setting(key, deflt) for key, deflt in Defaults]

    return Config(*tupvals)

def pushhook(node, hooktype, url, repo, source, ui, **kwargs):
    # pylint: disable=unused-argument,too-many-arguments

    config = get_config(ui)
    changesets = get_changesets(repo, node)
    count = len(changesets)
    messages = render_changesets(ui, repo, changesets, config)

    ensure_plural = "s" if count > 1 else ""

    webroot = web_path(repo.root, config)

    if config.repo_name is not None:
        ensure_repo_name = " to \"{0}\"".format(config.repo_name) if config.repo_name else ""
    else:
        ensure_repo_name = " to \"{0}\"".format(webroot)

    push_user = os.environ.get("LOGNAME") or ui.username()

    text = "{user} pushed {count} changeset{ensure_plural}{ensure_repo_name}:\n```{changes}```".format(
        user=push_user,
        count=count,
        ensure_plural=ensure_plural,
        ensure_repo_name=ensure_repo_name,
        changes=messages)
    num_hooks = len(config.webhook_urls.split())
    ui.status(_('slackhooks: submitting %d notification(s) to slack\n') % (num_hooks,))
    post_message_to_slack(text, config)


def get_changesets(repo, node):
    node_rev = repo[node].rev()
    tip_rev = repo['tip'].rev()
    return range(tip_rev, node_rev - 1, -1)


def render_changesets(ui, repo, changesets, config):
    url = config.commit_url

    webroot = web_path(repo.root, config)

    if url:
        url = url.format(reporoot=repo.root,
                         webroot=webroot,
                         reponame=config.repo_name,
                         rev="{node|short}")
        node_template = "<{url}|{{node|short}}>".format(url=url)
    else:
        node_template = "{node|short}"

    template = "{0}\\n".format(" | ".join([
        "{branch}",
        node_template,
        "{date(date, '%Y-%m-%d [%H:%M:%S]')}",
        "{author|user}",
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
        urllib2.build_opener().open(request)

def payload_optional_key(payload, config, key):
    value = config.__getattribute__(key)
    if value:
        payload[key] = value
