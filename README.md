# GeoTracker-Apple-Automation

This project presents a method for tracking iOS devices when they reach specific locations. In this repository, the focus is on tracking movement between work and home to gather insights for future analysis.

-----
### Overview

This app provides a way to monitor the timings of entering and leaving work and home locations using iPhones, which we carry with us every day and almost everywhere we go.

The solution requires three key components:

1) Simple infrastructure on AWS
2) iOS Shortcuts Automation App
3) Discord Webhook

#### AWS Infrastructure

The AWS infrastructure includes the following components:

- **DynamoDB**, A table named geo_tracking_ios stores the tracking data.
- **Lambda Function** This function handles POST requests and submits structured data to DynamoDB.
- **API Gateway** A public endpoint is created to connect with the Lambda function via the /geolog path.

------

### Lambda Function Setup


A Lambda function, geo_tracker_ios_automate, is invoked by calls to the API Gateway at /geolog.

![image](https://github.com/user-attachments/assets/3457dcfa-a31c-48e5-bc48-96bb4b617ee5)

#### Lambda Script Requirements

The script for the Lambda function requires a Discord [webhook url](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) to send notifications.

To deploy the script to Lambda with its dependencies, you need to install the necessary packages. This can be done with the following command:

```pip install --platform manylinux2014_x86_64 --target=package --implementation cp --python-version 3.12 --only-binary=:all: --upgrade package_name```

Place the Python script within the package directory and then zip the contents.

#### Lambda Function Input

The Lambda function accepts invocations with the following JSON body:

```json
{
    "longitude": "-XX.XXXX",
    "latitude": "XX.XXXX",
    "user": "name",
    "action": "ACTION_LABEL",
    "address": "123 Test Address"
}

```

The Lambda function, connected via API Gateway, processes different actions based on the ACTION_LABEL provided. The function has permissions to interact with DynamoDB and stores this information in the geo_tracking_ios table.

#### Available Actions

The ACTION_LABEL in the JSON body determines the action being tracked. The available actions are:

```bash
enter_work
leave_work
enter_home
leave_home
```

Based on the action, the system generates a human-readable message, e.g., "Michael has entered the workplace - timestamp. This has been recorded on AWS DynamoDB."

--------

### Example JSON Event Object for Lambda Recieved.
Here is an example of the typical event object received by Lambda:

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
#### Architecture Overview

The architecture of the system is illustrated below:

![image](https://github.com/user-attachments/assets/754b024a-74f2-45a0-9a04-51de2d2a60bb)


-------
#### iOS Automation Shortcut
Due to limitations on iOS, sharing automation shortcuts is not possible. Therefore, setting up the automation manually is necessary. Additionally, since location services are considered sensitive, all location-based automations require manual confirmation to run. This is acceptable if you regularly use your phone.

<p align="center">
  <img src="https://github.com/user-attachments/assets/8a18935a-8cba-42ad-850a-feace324d52f" width="45%" />
  <img src="https://github.com/user-attachments/assets/716ea1fc-00e1-4f3e-b867-7cb3e8dfba5c" width="45%" />
</p>


-------
#### Discord Webhook Notifications
The system can send notifications to a Discord channel, as shown below:

![image](https://github.com/user-attachments/assets/f85cc290-5a5b-4e77-b8a5-3bb302489aa6)


----
