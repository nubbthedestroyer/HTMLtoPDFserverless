import json
import urllib


def html(event, context):

    params = event['queryStringParameters']

    html = urllib.urlopen(params['template']).read()

    for i in params:
        # print(i)
        html = html.replace('{{' + i + '}}', params[i])

    body = html

    response = {
        "statusCode": 200,
        "body": body,
        "headers": {
            "content-type": "text/html",
        }
    }

    return response
    # context.succeed(response)