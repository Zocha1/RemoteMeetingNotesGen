# test_email.py
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import os
from dotenv import load_dotenv

load_dotenv()

SENDINBLUE_API_KEY = os.getenv('SENDINBLUE_API_KEY')
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_NAME = os.getenv('SENDER_NAME')

def send_test_email(recipient_email, subject, text_content):
    """
    Wysyła testowy e-mail za pomocą Sendinblue API.
    """
    try:
        # Configure API key authorization
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = SENDINBLUE_API_KEY
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

        # Create the email message
        html_content = f"""
            <html>
            <head><title>{subject}</title></head>
            <body>
                <h1>{subject}</h1>
                <p>{text_content}</p>
             </body>
            </html>
        """

        sender = {"name": SENDER_NAME, "email": SENDER_EMAIL}
        to = [{"email": recipient_email}]

        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=to,
            sender=sender,
            html_content=html_content,
            subject=subject
        )

        # Send email using Sendinblue API
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(f"Test email sent successfully, details: {api_response}")
    except ApiException as e:
        print(f"Error sending test email: {e}")
    except Exception as e:
          print(f"Error: {str(e)}")


if __name__ == "__main__":
    test_recipient_email = "heniek.kombajnista666@gmail.com"  # Zmień na swój adres email
    test_subject = "Test email from Sendinblue API"
    test_content = "This is a test email to verify the connection to Sendinblue."

    send_test_email(test_recipient_email, test_subject, test_content)