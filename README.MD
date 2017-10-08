## HTMLtoPDF in Lambda (Serverless)
##### A Serverless Framework based tool to fill in html templates and return either compiled HTML or a PDF from the compiled.

### Install

##### Requires some local dependencies, including

- Serverless Framework
- A serverless plugin called 'serverless-python-individually'
- Docker (for client side builds)


##### Run this to install the NPM stuff:
````
npm i serverless-python-individually
sudo npm i -g serverless
````

##### Docker install can be found here: https://www.docker.com/community-edition

### Deployment
##### Project can be deployed to an AWS environment like so:
````
sls deploy
````

### HTML Endpoint
##### The HTML endpoint give you the ability to pass a template URL and an unlimited number of query parameters to fill in the template.  Heres an example:
````
https://${apigatewayID}.execute-api.us-east-1.amazonaws.com/dev/html?vocative=John%20Smith&reference-number=1234567&current_date=Nov.%2013&template=https:%2F%2Fs3-us-west-2.amazonaws.com%2Fsellerletters%2FCover%2Bletter%2Bto%2Bseller%2Bwrap.html
````
##### In that case, the template URL is a html file located in S3.

### PDF Endpoint
##### This does the exact same as the HTML Endpoint, but it stores the filled in template as PDF in S3 and then passes a 302 redirect to the requester.
````
https://7gfa0ijd58.execute-api.us-east-1.amazonaws.com/dev/pdf?vocative=John%20Smith&reference-number=1234567&current_date=Nov.%2013&template=https:%2F%2Fs3-us-west-2.amazonaws.com%2Fsellerletters%2FCover%2Bletter%2Bto%2Bseller%2Bwrap.html
````