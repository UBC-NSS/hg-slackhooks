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

#. ``webhook_urls`` Space separated list of incoming-webhook URLs of the form ``"https://hooks.slack.com/services/FOO/BAR/BAZ"``. Each hook will be triggered in the order given.
#. ``repo_name`` is a name of your repository. *Optional.*  When the key is omitted, the name of the repo is inferred dynamically. It can be set to the empty string if one does not wish it printed.
#. ``commit_url`` will be used as the link URL for particular changeset. *Optional.* If it is specified, link to a changeset will be inserted in description of changeset. Plain text short revision number will be used otherwise. Occurrences of template variables ``{repo}`` and ``{rev}`` in the URL will be substituted by the name of the repository, and the revision id of the changeset, respectively.
#. ``username`` is the displayed name on slack. *It's optional.* Omitting this key, will allow the username from the incoming-webhook configuration to be displayed.
#. ``icon_emoji`` is the name of emoticon, which will be displayed. *It's optional.* You can use ``icon_url`` instead. 
#. ``icon_url`` is a direct link to image, which will be displayed. *It's optional.* You can use
   `this icon URL <https://raw.githubusercontent.com/oblalex/hg-slackhooks/master/assets/mercurial.png>`_ if you want.

``icon_emoji`` and ``icon_url`` are both optional and interchangeable.
