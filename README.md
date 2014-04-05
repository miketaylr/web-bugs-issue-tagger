# web-bugs issue tagger

A tiny app to listen for GitHub webhook Issues events (ignoring when issues are closed) and add labels.

When an issue is created in the [web-bugs](https://github.com/webcompat/web-bugs), usually via [webcompat.com](http://webcompat.com), the app looks for label metadata in the form of a special HTML comment: `<!-- @browser: firefox -->`, for example. If found, our friend @Neptr will add the label and a comment.

This repo assumes the following environment variables are set:

`USER_REPO`: in the format of `:user/:repo`
`OAUTH_TOKEN`: see [creating an access token for command line use](https://help.github.com/articles/creating-an-access-token-for-command-line-use)

You can test things locally using a `payload.json` file:

`python app.py` to start the server.

``` bash
curl -X POST \
      -H 'content-type: application/json' \
      -H 'X-GitHub-Event: issues' \
      -d @payload.json
      http://localhost:5000/turkeysandwiches
```