import boto3
import json
import time

sqs = boto3.client('sqs')
s3 = boto3.client('s3')
queue_url = 'https://sqs.us-east-1.amazonaws.com/769180238555/free-queue'


def edit_file(input_file_name, output_file_name):
    with open(input_file_name, 'r') as input_file, open(output_file_name, 'w') as output_file:
        # Read the contents of the input file
        contents = input_file.read()

        # Split the contents by comma
        split_contents = contents.split(',')

        # Write the split contents to the output file
        for item in split_contents:
            output_file.write(item.strip() + '\n')


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
            body = json.loads(message['Body'])
            body_message = json.loads(body['Message'])
            file_name = body_message['Records'][0]['s3']['object']['key']
            print(f'File name: {file_name}')

            s3.download_file('s3-with-sns-sqs', file_name, 's3_file.txt')
            print("file downloaded successfully")

            edit_file('s3_file.txt', 'output.txt')
            print("file updated successfully")

            try:
                response = s3.upload_file('output.txt', 's3-with-sns-sqs', f'after/names{i}.txt')
            except ClientError as e:
                print(e)
                print('Error in uploading')
            print("file uploaded successfully")

            receipt_handle = message['ReceiptHandle']
            sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
            print("message deleted from queue successfully")
        else:
            print('No messages in the queue')
        time.sleep(10)
        i += 1

