import boto3
import json
import csv
import time

sqs = boto3.client('sqs')
queue_url = 'https://sqs.us-east-1.amazonaws.com/769180238555/queue-with-dead'

if __name__ == '__main__':
    i = 1
    while True:
        print(f"cycle: {i}")

        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=1,
            VisibilityTimeout=0,
            WaitTimeSeconds=0
        )

        if 'Messages' in response:
            message = response['Messages'][0]

            with open('metadata.csv', 'w', newline='') as file:
                # Create a CSV writer object
                writer = csv.writer(file)

                # Write the dictionary to the CSV file
                for key, value in message.items():
                    if key != 'Body':
                        writer.writerow([key, value])
            print("metadata file has created successfully")

            receipt_handle = message['ReceiptHandle']
            sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
            print("message deleted from queue successfully")

        else:
            print('No messages in the queue')
        time.sleep(10)
        i += 1
