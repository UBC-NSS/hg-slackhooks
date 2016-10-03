hg-slackhooks
=============

Mercurial server-side hook for notifying Slack of new commits. The
hook is compatible with standalone/local repos, and repos managed centrally
with mercurial-server.

Examples
~~~~~~~~

To add push hooks for some repo, modify ``.hg/hgrc`` in the repository
receiving changesets::

    [slackhooks]
    webhook_urls = INCOMING_WEBHOOK_URL1 ...

    # Omit this to derive the name from the repository absolute path.
    repo_name = Repository Name.

    # Number of leading slashes to remove from the repo path to form
    # a web-usable path.
    web_strip = 0

    # Optional templated URL. Adds a changeset view link
    # See documentation below for available variables.
    commit_url = http://myrepos.com/hg/{repoweb}/rev/{rev}

    # Optional settings to override Slack's webhook sender information.
    #username = Mercurial
    #icon_emoji = :ghost:
    #icon_url = http://i.imgur.com/Ivcctgq.png

    [hooks]
    changegroup.slackhooks= python:/path/to/slackhooks.py:pushhook

Example of output on Slack:

.. image:: http://imgur.com/1omf7Mh
    :alt: Mercurial push hook chat message
    :align: center

Options
~~~~~~~

#. ``webhook_urls`` Space separated list of incoming-webhook URLs of the form ``"https://hooks.slack.com/services/FOO/BAR/BAZ"``. Each hook will be triggered in the order given. The mercurial config file syntax allows those to be specified on multiple lines, as long as the following lines are indented.
#. ``repo_name`` is a name of your repository. *Optional.*  When the key is omitted, the name of the repo is inferred from the path of the repository. It can also be set to the empty string if one does not wish it printed.
#. ``web_strip`` Number of leading slashes (``/``) to remove from the absolute path of the repo to form a web-friendly path. *Optional.* Default is 0. The path with the prefix removed can be referenced with the template variable ``{webroot}``.
#. ``commit_url`` will be used as the link URL for particular changeset. *Optional.* If it is specified, link to a changeset will be inserted in description of changeset. Plain text short revision number will be used otherwise. Template variable ``{reporoot}`` is substituted with the absolute path of the repo, ``{webroot}`` with the web-safe path of the repo, ``{reponame}`` the configured repository name, and ``{rev}`` with the revision id of the changeset.
#. ``username`` is the displayed name on slack. *It's optional.* Omitting this key, will allow the username from the incoming-webhook configuration (on Slack) to be displayed.
#. ``icon_emoji`` is the name of emoticon, which will be displayed. *It's optional.* You can use ``icon_url`` instead. 
#. ``icon_url`` is a direct link to image, which will be displayed. *It's optional.* You can use
   `this icon URL <https://raw.githubusercontent.com/oblalex/hg-slackhooks/master/assets/mercurial.png>`_ if you want.

``icon_emoji`` and ``icon_url`` are both optional and interchangeable.
