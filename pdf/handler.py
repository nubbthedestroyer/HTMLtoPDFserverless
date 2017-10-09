import urllib
import os
import uuid
import boto3
import pdfkit
import logging

boto3.set_stream_logger('boto3.resources', logging.DEBUG)
s3 = boto3.resource('s3')


def pdf(event, context):

    # some variables
    guid_tag = str(uuid.uuid4())
    pdf_name = guid_tag + '.pdf'
    pdf_file = '/tmp/' + pdf_name
    s3_key = 'pdfs/' + pdf_name
    location = 'https://s3.amazonaws.com/' + os.environ['bucketname'] + '/' + s3_key

    print('pdf_name = ' + pdf_name)
    print('pdf_file = ' + pdf_file)
    print('s3_key = ' + s3_key)
    print(location)

    # build html object
    params = event['queryStringParameters']
    print(params['template'])

    html = urllib.urlopen(params['template']).read()

    for i in params:
        # print(i)
        html = html.replace('{{' + i + '}}', params[i])

    # body = html

    # setup wkhtmltopdf binary
    os.system('rm -rf /tmp/wkhtmltopdf')
    os.system('cp wkhtmltopdf /tmp/')
    os.system('chmod +x /tmp/wkhtmltopdf')

    # set some pdfkit options
    config = pdfkit.configuration(wkhtmltopdf='/tmp/wkhtmltopdf')
    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'no-outline': None,
        # 'dpi': 96
        'print-media-type': True,
        # 'enable-smart-shrinking': True
    }

    pdfkit.from_string(html, pdf_file,
                       options=options,
                       configuration=config)

    s3.meta.client.upload_file(pdf_file, os.environ['bucketname'], s3_key)
    s3.meta.client.put_object_acl(ACL='public-read', Bucket=os.environ['bucketname'], Key=s3_key)

    response = {
        "statusCode": 302,
        "body": '',
        "headers": {
            "Location": location,
            # "content-type": "application/json",
        }
    }

    return response
