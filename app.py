#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import os
import re
import requests
from flask import Flask, abort, request

app = Flask(__name__)


def api_post(endpoint, payload, issue):
    '''Helper method to post junk to GitHub. Assumes a USER_REPO and
    OAUTH_TOKEN environment variable exist.'''
    repo = os.environ['USER_REPO']
    headers = {'Authorization': 'token {0}'.format(os.environ['OAUTH_TOKEN'])}
    uri = 'https://api.github.com/repos/{0}/issues/{1}/{2}'.format(repo,
                                                                   issue,
                                                                   endpoint)
    requests.post(uri, data=json.dumps(payload), headers=headers)


def parse_label(body, issue_number):
    '''Parse the labels from the body in comments like so:
    <!-- @browser: value -->. Currently this only handles a single label,
    becuase that's all that we set in webcompat.com.

    So, CAVEAT EMPTOR, or whatever.'''
    match_list = re.search(r'<!--\s@(\w+):\s(\w+)\b', body)
    if match_list:
        # perhaps we do something more interesting depending on
        # what groups(n)[0] is in the future.
        # right now, match_list.groups(0) should look like:
        # ('browser', 'firefox')
        set_label(match_list.groups(0)[1].lower(), issue_number)


def set_label(label, issue_number):
    '''Do a GitHub POST request using one of our bots, which has push access
    and set a label for the issue. Then leave a comment.'''
    # POST /repos/:owner/:repo/issues/:number/labels
    # ['Label1', 'Label2']
    payload = [label]
    api_post('labels', payload, issue_number)
    comment_on_issue(label, issue_number)


def comment_on_issue(label, issue_number):
    '''Comment that a label was added. This will get annoying undoubtedly.'''
    # POST /repos/:owner/:repo/issues/:number/comments
    # {"body": "a new comment"}
    payload = {"body":
               "Greetings, creator! I added a {0} label for you.".format(
                   label)}
    api_post('comments', payload, issue_number)


@app.route('/')
def index():
    '''Go away.'''
    return abort(403)


# It's a secret to everyone.
@app.route('/turkeysandwiches', methods=['GET', 'POST'])
def hooklistener():
    '''Listen for the "issues" webhook event, parse the body,
       post back labels. But only do that for the 'opened' action.'''
    if request.method == 'GET':
        return abort(403)
    elif (request.method == 'POST' and
            request.headers.get('X-GitHub-Event') == 'issues'):
        payload = json.loads(request.data)
        if payload.get('action') == 'opened':
            issue_body = payload.get('issue')['body']
            issue_number = payload.get('issue')['number']
            parse_label(issue_body, issue_number)
            return 'gracias, amigo.'
        else:
            return 'cool story, bro.'
    elif (request.method == 'POST' and
            request.headers.get('X-GitHub-Event') == 'ping'):
        return 'pong'

if __name__ == "__main__":
    app.run(debug=True)
