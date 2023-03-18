import termcolor
import boto3
import json
import sys
import time

class DocumentProcessor:

    def __init__(self, bucket, document, region):
        self.bucket = bucket
        self.document = document
        self.region_name = region

        self.textract = boto3.client('textract', region_name=self.region_name)
        self.sqs = boto3.client('sqs')
        self.sns = boto3.client('sns')

    def ProcessDocument(self):
        jobFound = False

        response = self.textract.start_lending_analysis(
            DocumentLocation={'S3Object': {'Bucket': self.bucket, 'Name': self.document}})
        print('Processing type: Analysis')

        print('Start Job Id: ' + response['JobId'])
        dotLine = 0
        # while not jobFound:
        #     print('.', end='')
            # import time
            # time.sleep(5)
            # if sqsResponse := self.sqs.receive_message(
            #     QueueUrl=self.sqsQueueUrl,
            #     MessageAttributeNames=['ALL'],
            #     MaxNumberOfMessages=10,
            # ):
            #     if 'Messages' not in sqsResponse:
            #         if dotLine < 40:
            #             print('.', end='')
            #             dotLine = dotLine + 1
            #         else:
            #             print()
            #             dotLine = 0
            #         sys.stdout.flush()
            #         time.sleep(5)
            #         continue

            #     for message in sqsResponse['Messages']:
            #         notification = json.loads(message['Body'])
            #         textMessage = json.loads(notification['Message'])
            #         print(textMessage['JobId'])
            #         print(textMessage['Status'])
            #         if str(textMessage['JobId']) == response['JobId']:
            #             print('Matching Job Found:' + textMessage['JobId'])
            #             jobFound = True
            #             self.GetResults(textMessage['JobId'])
            #             self.GetSummary(textMessage['JobId'])
            #             self.sqs.delete_message(QueueUrl=self.sqsQueueUrl,
            #                                     ReceiptHandle=message['ReceiptHandle'])
            #         else:
            #             print("Job didn't match:" +
            #                   str(textMessage['JobId']) + ' : ' + str(response['JobId']))
            #         # Delete the unknown message. Consider sending to dead letter queue
            #         self.sqs.delete_message(QueueUrl=self.sqsQueueUrl,
            #                                 ReceiptHandle=message['ReceiptHandle'])

        print('Done!')

    def CreateTopicandQueue(self):

        millis = str(int(round(time.time() * 1000)))

        # Create SNS topic
        snsTopicName = f"AmazonTextractTopic{millis}"

        topicResponse = self.sns.create_topic(Name=snsTopicName)
        self.snsTopicArn = topicResponse['TopicArn']

        # create SQS queue
        sqsQueueName = f"AmazonTextractQueue{millis}"
        self.sqs.create_queue(QueueName=sqsQueueName)
        self.sqsQueueUrl = self.sqs.get_queue_url(QueueName=sqsQueueName)['QueueUrl']

        attribs = self.sqs.get_queue_attributes(QueueUrl=self.sqsQueueUrl,
                                                AttributeNames=['QueueArn'])['Attributes']

        sqsQueueArn = attribs['QueueArn']

        # Subscribe SQS queue to SNS topic
        self.sns.subscribe(
            TopicArn=self.snsTopicArn,
            Protocol='sqs',
            Endpoint=sqsQueueArn)

        # Authorize SNS to write SQS queue
        policy = """{{
  "Version":"2012-10-17",
  "Statement":[
    {{
      "Sid":"MyPolicy",
      "Effect":"Allow",
      "Principal" : {{"AWS" : "*"}},
      "Action":"sqs:*",
      "Resource": "{}",
      "Condition":{{
        "ArnEquals":{{
          "aws:SourceArn": "{}"
        }}
      }}
    }}
  ]
}}""".format(sqsQueueArn, self.snsTopicArn)

        response = self.sqs.set_queue_attributes(
            QueueUrl=self.sqsQueueUrl,
            Attributes={
                'Policy': policy
            })

    def DeleteTopicandQueue(self):
        self.sqs.delete_queue(QueueUrl=self.sqsQueueUrl)
        self.sns.delete_topic(TopicArn=self.snsTopicArn)

    # Display information about a block
    def DisplayExtractInfo(self, response):
        print(response)
        results = response['Results']
        for page in results:
            print(f'Page Classification: {page["PageClassification"]["PageType"]}')
            print(f'Page Number: {page["Page"]}')
            

    def GetSummary(self, jobId):
        
        maxResults = 1000
        response = self.textract.get_lending_analysis_summary(JobId='32d95d2b005c281cf23c5bc350a69cd44861fb13e9dabfb4c93e36b8acf9d8d9')
        print('Detected Document Text')
        print(f"Pages: {response['DocumentMetadata']['Pages']}")
        print("Summary info:")
        # print(response)
        

    def GetResults(self, jobId):

        maxResults = 1000
        paginationToken = None
        finished = False

        while not finished:

            response = None
            response = self.textract.get_lending_analysis(JobId='32d95d2b005c281cf23c5bc350a69cd44861fb13e9dabfb4c93e36b8acf9d8d9'
                                                          )
            print('Detected Document Text')
            # print(f"Pages: {response['DocumentMetadata']['Pages']}")

            self.DisplayExtractInfo(response)

            if 'NextToken' in response:
                paginationToken = response['NextToken']
            else:
                finished = True
        return response
import termcolor
def main():
    # roleArn = ''
    bucket = 'enium-admissions-document-textract'
    document = 'melissa_rendon_license.png'
    region_name = 'us-east-1'
    
    analyzer = DocumentProcessor(bucket, document, region_name)

    # analyzer.ProcessDocument()
    # analyzer.DeleteTopicandQueue()
    
    # analyzer.GetSummary(analyzer.ProcessDocument())
    t = analyzer.GetResults(analyzer.ProcessDocument())
    # convert to json
    import json
    t = json.dumps(t)
    # pretty print json
    print(json.dumps(json.loads(t), indent=4, sort_keys=True))

    # parse json
    t = json.loads(t)
    print(t['Results'][0]['PageClassification']['PageType'])
    # {
    # "AnalyzeLendingModelVersion": "1.0",
    # "DocumentMetadata": {
    #     "Pages": 1
    # },
    # "JobStatus": "SUCCEEDED",
    # "ResponseMetadata": {
    #     "HTTPHeaders": {
    #         "content-length": "2590",
    #         "content-type": "application/x-amz-json-1.1",
    #         "date": "Sun, 12 Feb 2023 18:35:37 GMT",
    #         "x-amzn-requestid": "2ab56584-b5f8-4807-b112-98d8c9f6becf"
    #     },
    #     "HTTPStatusCode": 200,
    #     "RequestId": "2ab56584-b5f8-4807-b112-98d8c9f6becf",
    #     "RetryAttempts": 0
    # },
    # "Results": [
    #     {
    #         "Extractions": [
    #             {
    #                 "IdentityDocument": {
    #                     "IdentityDocumentFields": [
    #                         {
    #                             "Type": {
    #                                 "Text": "FIRST_NAME"
    #                             },
    #                             "ValueDetection": {
    #                                 "Confidence": 96.49171447753906,
    #                                 "Text": "MELISSA"
    #                             }
    #                         },
    #                         {
    #                             "Type": {
    #                                 "Text": "LAST_NAME"
    #                             },
    #                             "ValueDetection": {
    #                                 "Confidence": 96.00674438476562,
    #                                 "Text": "RENDON"
    fields = t['Results'][0]['Extractions'][0]['IdentityDocument']['IdentityDocumentFields']
    for field in fields:
        # if the text is not empty
        if field['ValueDetection']['Text']:
            print(termcolor.colored(field['Type']['Text'], 'red'), field['ValueDetection']['Text'])
                        

# b id = 5d6d58da7a96163d59b0234b14de71b6a806badbe2bca61611995fe8ce39add0
if __name__ == "__main__":
    main()


id

FIRST_NAME
LAST_NAME
EXPIRATION_DATE
ID_TYPE

income
NAME
YEAR
YTD GROSS PAY
YTD NET PAY
PAY DATE
CURRENT NET PAY
CURRENT GROSS PAY



SOLAR CONTRACT
BORROW NAME
PROPERTY ADDRESS
COMPANY NAME
SIGNED