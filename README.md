# web-bugs issue tagger

This repo assumes you have the following environment variables set:

`USER_REPO`: in the format of `:user/:repo`
`OAUTH_TOKEN`: see https://help.github.com/articles/creating-an-access-token-for-command-line-use

You can test things locally using the `payload.json` file:

`python app.py` to star the server.

`curl -X POST -H 'content-type: application/json' -H 'X-GitHub-Event: issues' -d @payload.json http://localhost:5000/turkeysandwiches`