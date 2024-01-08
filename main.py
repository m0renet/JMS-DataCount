import os
import json
import boto3
import requests
import datetime

def lambda_handler(event, context):
    # AWS SNS setup
    sns = boto3.client('sns')
    topic_arn = os.getenv('SNS_TOPIC_ARN')  # make sure this is set in your Lambda function's environment variables

    # API URL
    url = 'Subscribe api link'

    # Send request
    response = requests.get(url)

    # Parse JSON response
    data = response.json()

    # Calculate remaining bandwidth
    total_bw = data['monthly_bw_limit_b']
    used_bw = data['bw_counter_b']
    remaining_bw = total_bw - used_bw

    # Calculate days until next reset
    today = datetime.date.today()
    if today.month == 12:
        next_reset_date = datetime.date(today.year + 1, 1, 1)
    else:
        next_reset_date = datetime.date(today.year, today.month + 1, 1)
    days_until_reset = (next_reset_date - today).days

    # Create message
    message = f"Hello, our Just My Socks subscription status this month is as follows:\nTotal bandwidth: {total_bw / 1e9} GB\nUsed bandwidth: {round(used_bw / 1e9, 1)} GB\nRemaining bandwidth: {round(remaining_bw / 1e9, 1)} GB\nDays until next reset: {days_until_reset}\nOur subscription reset date is the 1st of every month (UTC -8 / Los Angeles time zone)"

    # Send SNS notification
    sns.publish(
        TopicArn=topic_arn,
        Message=message,
        Subject='IT7-JustMySocks Bandwidth Usage Count'
    )

    return {
        'statusCode': 200,
        'body': json.dumps('SNS notification sent!')
    }
