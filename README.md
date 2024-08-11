# GeoTracker-Apple-Automation
This will aim to present a way to track iOS devices when reaching a specific location, for this repository, it is tracking when I go between work and my home, for some cool insights in the future.

-----

This app aims to provide a method of tracking timings of entering, leaving work and home locations, through the use of our iPhones, something we carry with us everyday, and usually everywhere we go.

The solution requires three things, 1) simple infrastructure on AWS, 2) iOS Automations Shortcut App and 3) Discord Webhook

The simple infrastructure includes:

- **DynamoDB**, this will store this within a table named `geo_tracking_ios`.
- **Lambda Function** for running the handling POST requests and submitting structured data to a `DynamoDB`.
- **API Gateway** this created the specific endpoint publicly to be connected, connecting to the lambda with endpoint path `/geolog`.

------

Creation of a Lambda function, `geo_tracker_ios_automate` which is invoked by a call to API Gateway `/geolog`, 

![image](https://github.com/user-attachments/assets/3457dcfa-a31c-48e5-bc48-96bb4b617ee5)

The script used for the lambda function requires the addition of a discord [webhook url](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks),

In order to submit this to lambda, this must be zipped with dependencies, in order to do this, you must install requests, which is done with the following command.

```pip install --platform manylinux2014_x86_64 --target=package --implementation cp --python-version 3.12 --only-binary=:all: --upgrade package_name```

Put the python script and put this within the package directory and then zip this file.

The function will take invokations with the following inputs, 

JSON Body:

```bash
{
    "longitude": "-XX.XXXX",
    "latitude": "XX.XXXX",
    "user": "name",
    "action": "ACTION_LABEL",
    "address": "123 Test Address"
}

```

Here this will be passed to the node, in which different actions can be passed, the lambda has permissions to interact with DynamoDB

It should add this information to the database with table name, geo_tracking_ios, the lambda should use python, simply listening for these requests, as the lambda is connected to via API gateway, and storing this information,

For this system, the following ACTION_LABEL is available,

The message will be dependant on the action send, for example the four different states available are:

```bash
enter_work
leave_work
enter_home
leave_home
```

This should be handled nicely to present human readable messages like "Michael" title case user attribute, "has entered the workplace - timestamp, this has been recorded on AWS DynamoDB"

--------

#### Example JSON Event Object for Lambda Recieved.
This is the typical object with the following path and object,

```json
{
  "version": "2.0",
  "routeKey": "POST /geolog",
  "rawPath": "/geolog",
  "rawQueryString": "",
  "headers": {
    "accept": "*/*",
    "content-type": "application/json",
    "host": ".execute-api.eu-north-1.amazonaws.com",
    "user-agent": "PostmanRuntime/7.40.0",
    "x-amzn-trace-id": "Root=1-",
    "x-forwarded-for": "",
    "x-forwarded-port": "443",
    "x-forwarded-proto": "https"
  },
  "requestContext": {
    "accountId": "",
    "apiId": "",
    "domainName": ".execute-api.eu-north-1.amazonaws.com",
    "domainPrefix": "",
    "http": {
      "method": "POST",
      "path": "/geolog",
      "protocol": "HTTP/1.1",
      "sourceIp": "",
      "userAgent": "PostmanRuntime/7.40.0"
    },
    "requestId": "=",
    "routeKey": "POST /geolog",
    "stage": "$default",
    "time": "02/Aug/2024:10:22:35 +0000",
    "timeEpoch": 1722594155011
  },
  "body": "{\"longitude\": \"-XX.XXXX\", \"latitude\": \"XX.XXXX\", \"user\": \"michael\", \"action\": \"enter_work\", \"address\": \"123 Test Address\"}",
  "isBase64Encoded": false
}
```


------

The architecture is shown below,

![image](https://github.com/user-attachments/assets/754b024a-74f2-45a0-9a04-51de2d2a60bb)


-------
#### iOS Automation Shortcut
There is no sharing ability on iOS automation, so manual filling of this is neccesary, in addition to this, limitation of this system, as automations including location services is deemed sensitive and possibly a safety risk, all automations must be run manually by accepting the run button, this is fine if you are using your phone on a constant basis.

<p align="center">
  <img src="https://github.com/user-attachments/assets/8a18935a-8cba-42ad-850a-feace324d52f" width="45%" />
  <img src="https://github.com/user-attachments/assets/716ea1fc-00e1-4f3e-b867-7cb3e8dfba5c" width="45%" />
</p>


-------
#### Discord Webhook Notifications
This can be shown on a discord channel as shown,

![image](https://github.com/user-attachments/assets/f85cc290-5a5b-4e77-b8a5-3bb302489aa6)


----
