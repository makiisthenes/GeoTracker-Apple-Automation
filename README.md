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

------


