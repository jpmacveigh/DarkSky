import json
import boto3
from botocore.exceptions import ClientError
def send_mail(liste_destinataires,objet,message):
    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    SENDER = "jpmacveigh@hotmail.fr"
    # Replace recipient@example.com with a "To" address. If your account 
    # is still in the sandbox, this address must be verified.
    #RECIPIENT = "jpmacveigh@gmail.com"
    # Specify a configuration set. If you do not want to use a configuration
    # set, comment the following variable, and the 
    # ConfigurationSetName=CONFIGURATION_SET argument below.
    #CONFIGURATION_SET = "ConfigSet"
    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "eu-west-1"
    # The subject line for the email.
    SUBJECT = "Essai send_mail"
    SUBJECT = objet
    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = """Amazon SES Test JPMV (Python)\r\n
                 This email was sent with Amazon SES using the
                 AWS SDK for Python (Boto)."""
    BODY_TEXT=message
    # The HTML body of the email.
    BODY_HTML ="""<html>
    <head></head>
    <body>
        <p>"""+BODY_TEXT+"""</p>        
        <p>This email was sent with
        <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
        <a href='https://aws.amazon.com/sdk-for-python/'>
          AWS SDK for Python (Boto)</a>.</p>
    </body>
    </html>
    """
    # The character encoding for the email.
    CHARSET = "UTF-8"
    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)
    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': liste_destinataires,
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            #ConfigurationSetName=CONFIGURATION_SET,
        )
    except ClientError as e:         # Display an error if something goes wrong.	
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
        return {
          'statusCode': 200,
          'body': "mail envoyé"
        }        

message="Bonjour tout le monde!,<br>Je vous souhaite une bonne année<br>et une bonne santé."  
send_mail(["jpmacveigh@gmail.com",],"Essai",message)  

