import urllib
import os
import uuid
import boto3
import logging
import hashlib

boto3.set_stream_logger('boto3.resources', logging.DEBUG)
s3 = boto3.resource('s3')


def healthcheck(event, context):

    # some variables
    guid_tag = str(uuid.uuid4())
    pdf_name = guid_tag + '.pdf'
    html_name = guid_tag + '.html'
    pdf_file = '/tmp/' + pdf_name
    html_file = '/tmp/' + html_name
    pdf_key = 'pdfs/' + pdf_name
    html_key = 'html/' + html_name
    location = 'https://s3.amazonaws.com/' + os.environ['bucketname'] + '/' + pdf_key
    html_location = 'https://s3.amazonaws.com/' + os.environ['bucketname'] + '/' + html_key
    chrome_location = 'https://7rlphgn9o6.execute-api.us-west-2.amazonaws.com/dev/chrome?url=' + html_location
    check_url = 'https://s3.amazonaws.com/' + os.environ['bucketname'] + '/' + 'status-template.html'

    print('pdf_name = ' + pdf_name)
    print('pdf_file = ' + pdf_file)
    print('s3_key = ' + pdf_key)
    print(location)

    # build html object
    params = {
        'status': 'Healthy',
        'template': check_url
    }
    print(params['template'])

    html = urllib.urlopen(params['template']).read()

    for i in params:
        # print(i)
        html = html.replace('{{' + i + '}}', params[i])

    f = open(html_file, 'w')
    f.write(html)
    f.close()

    s3.meta.client.upload_file(html_file, os.environ['bucketname'], html_key, ExtraArgs={'ContentType': "text/html", 'ACL': "public-read"})
    s3.meta.client.put_object_acl(ACL='public-read', Bucket=os.environ['bucketname'], Key=html_key)

    built_hash = urllib.urlopen(chrome_location).read()

    print(built_hash)
    m = hashlib.md5()
    m.update(built_hash)
    print(m.hexdigest())

    # print(built_hash)

    response = {
        "statusCode": 302,
        "body": '',
        "headers": {
            "Location": chrome_location
        }
    }

    return response
