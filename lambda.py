import json
import boto3
import requests
from datetime import datetime
import uuid

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('geo_tracking_ios')

# Discord webhook URL
DISCORD_WEBHOOK_URL = ""  # Add Discord Webhook URL here.

def lambda_handler(event, context):
    try:
        # Parse the incoming JSON body
        body = json.loads(event['body'])
        
        # Extract required fields
        longitude = body.get('longitude')
        latitude = body.get('latitude')
        user = body.get('user')
        action = body.get('action')
        address = body.get('address')
        
        # Validate required fields
        missing_fields = [field for field in ['longitude', 'latitude', 'user', 'action', 'address'] if not body.get(field)]
        if missing_fields:
            error_message = f"Missing required fields: {', '.join(missing_fields)}"
            print(error_message)  # Log the missing fields
            return {
                'statusCode': 400,
                'body': json.dumps(error_message)
            }
        
        
        # Get current timestamp
        timestamp = datetime.now().isoformat()
        
        # Generate a unique ID for the item
        item_id = str(uuid.uuid4())
        
        # Store data in DynamoDB
        item = {
            'id': item_id,  # Add this line to include a unique identifier
            'user': user,
            'timestamp': timestamp,
            'longitude': longitude,
            'latitude': latitude,
            'action': action,
            'address': address
        }
        table.put_item(Item=item)
        
        # Generate Discord message
        message = generate_discord_message(user, action, timestamp)
        
        # Send message to Discord
        send_discord_message(message)
        
        return {
            'statusCode': 200,
            'body': json.dumps('Data processed successfully')
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Internal server error. Error: {str(e)}')
        }

def generate_discord_message(user, action, timestamp):
    user_title = user.title()
    action_messages = {
        'enter_work': f"{user_title} has entered the workplace",
        'leave_work': f"{user_title} has left the workplace",
        'enter_home': f"{user_title} has arrived home",
        'leave_home': f"{user_title} has left home"
    }
    
    action_message = action_messages.get(action, f"{user_title} performed an unknown action")
    return f"{action_message} - {timestamp}. This has been recorded on AWS DynamoDB."

def send_discord_message(message):
    payload = {
        'content': message
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(DISCORD_WEBHOOK_URL, data=json.dumps(payload), headers=headers)
    if response.status_code != 204:
        print(f"Failed to send Discord message. Status code: {response.status_code}")
