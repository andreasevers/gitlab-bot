# Gitlab Bot

Heavily based on <https://beenje.github.io/blog/posts/building-a-gitlab-bot-using-gidgetlab-and-aiohttp/>.

## Prerequisites

You need a way for GitLab to talk to your Python webserver.
If you deploy this on the same server as your GitLab instance, or you expose this behind a DNS, you can skip the Ngrok step.

### Ngrok

Ngrok exposes local servers behind NATs and firewalls to the public internet over secure tunnels. It's an easy way to test locally a webservice.

Check the installation instructions from the website. Note that for simple tests, you don't have to register an account.

If you have the Python webserver running locally on port 8080 (see later sections), you can expose it by running:

```bash
ngrok http 8080
```

Something similar will appear:

```
ngrok by @inconshreveable                                       (Ctrl+C to quit)

Session Status                online
Session Expires               7 hours, 59 minutes
Version                       2.2.8
Region                        United States (us)
Web Interface                 http://127.0.0.1:4040
Forwarding                    http://fb7fec7c.ngrok.io -> localhost:8080
Forwarding                    https://fb7fec7c.ngrok.io -> localhost:8080
```

You can access your local webservice using HTTP and even HTTPS!

```
curl -X GET https://fb7fec7c.ngrok.io
```

This address can be accessed from anywhere!. You could give it to a friend or use it as a GitLab webhook.

Ngrok even gives you a web interface on the port 4040 that allows you to inspect all the requests made to the service. Just open http://127.0.0.1:4040 in your browser.

If your bot is still running and you tried to send a GET, you should get a 405 as reply. Only POST methods are handled by the bot.

If you don't have any service listening on port 8080 and try to access the URL given by ngrok, you'll get a 502.

### Add the GitLab Webhook

Now that we have a local webservice that can receive requests thanks to ngrok, let's create a webhook on GitLab. If you haven't done so yet, create your own project on GitLab.

Go to your project settings and select Integrations to create a webhook:

- In the URL field, enter the ngrok URL you got earlier.
- For security reasons, type in some random characters under Secret Token (you can use Python secrets.token_hex(16) function)
- Under Trigger, select Issues events, Comments and Merge request events
- Leave Enable SSL verification enabled
- Click Add webhook

### Update the Config Variables in your environment

First, export the secret webhook token you just created:

```bash
export GL_SECRET=<secret token>
```

Then, if not already done, export your GitLab personal access token:

```bash
export GL_ACCESS_TOKEN=<access token>
```

## How to run as simple Python script

```bash
python3.6 -m pip install gidgetlab[aiohttp]
```

```bash
python3 bot.py
======== Running on http://0.0.0.0:8080 ========
(Press CTRL+C to quit)
```

## How to run on Cloud Foundry

*Only for airgapped Cloud Foundry:*

```bash
mkdir -p vendor
pip download -r requirements.txt --no-binary=:none: -d vendor
```

```bash
cf push
```

## How to build with Docker

```bash
docker build -t gitlabbot .
```

## How to run with Docker

With environment variables set in the Dockerfile:
```bash
docker run -p 8080:8080 -e gitlabbot
```

With environment variables set in the run command:
```bash
docker run -p 8080:8080 -e "GL_ACCOUNT=andreasevers" -e "GL_ACCESS_TOKEN=_xDnW3ey38c7dx76d7Ga" -e "GL_SECRET=ngrok" gitlabbot
```

