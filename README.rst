hg-slackhooks
=============

Mercurial server-side hooks for Slack messaging service.

Examples
~~~~~~~~

To add push hooks for some repo, modify ``.hg/hgrc`` in the central repository::

    [slackhooks]
    webhook_urls = INCOMING_WEBHOOK_URL1 ...
    repo_name = sample repository
    commit_url = http://myrepos.com/hg/{repo}/rev/{rev}
    icon_emoji = :mercurial:

    [hooks]
    changegroup.slackhooks= python:/path/to/slackhooks.py:pushhook

Example of chat message output:

.. image:: http://i.imgur.com/Ivcctgq.png
    :alt: Mercurial push hook chat message
    :align: center

Options
~~~~~~~

#. ``webhook_urls`` Space separated list of incoming-webhook urls
                    (e.g. https://hooks.slack.com/services/FOO/BAR/BAZ
                    ). The same content is sent to all of
                    them. Multiple hooks can be triggered with one
                    section that way.
#. ``repo_name`` is a name of your repository. *It's optional.*  When the key is omitted, the name of the repo is
                 inferred dynamically. Set to empty string if you don't want it printed.
#. ``commit_url`` is a part of URL for parcilular changeset. If it is specified, link to a changeset will be inserted in description of changeset. Plain text short revision number will be used otherwise. Templated for ``{repo}`` and ``{rev}``.
#. ``username`` is the displayed name. The default is to leave unspecified, which will use the username from the incoming-webhook configuration.
#. ``icon_emoji`` is the name of emoticon, which will be displayed. *It's optional.* You can use ``icon_url`` instead.
#. ``icon_url`` is a direct link to image, which will be displayed. *It's optional.* You can use
   `this icon URL <https://raw.githubusercontent.com/oblalex/hg-slackhooks/master/assets/mercurial.png>`_ if you want.

``icon_emoji`` and ``icon_url`` are both optional and interchangeable.
