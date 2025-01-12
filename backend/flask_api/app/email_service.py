# email_service.py
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import os
from dotenv import load_dotenv

load_dotenv()



def send_meeting_notes_email(recipients, meeting_title, transcription, summary):
    """
    Wysyła e-mail z notatkami ze spotkania za pomocą Sendinblue API.
    """
    SENDINBLUE_API_KEY = os.getenv('SENDINBLUE_API_KEY')
    SENDER_EMAIL = os.getenv('SENDER_EMAIL')
    SENDER_NAME = os.getenv('SENDER_NAME')
    try:
        # Configure API key authorization
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = SENDINBLUE_API_KEY
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

        # Create the email message
        html_content = f"""
            <html>
            <head><title>Meeting Notes: {meeting_title}</title></head>
            <body>
                <h1>Meeting Notes: {meeting_title}</h1>
                <h2>Transcription:</h2>
                <p>{transcription}</p>
                 <h2>Summary:</h2>
                <p>{summary}</p>
             </body>
            </html>
        """

        sender = {"name": SENDER_NAME, "email": SENDER_EMAIL}
        to = [{"email": recipient} for recipient in recipients]

        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=to,
            sender=sender,
            html_content=html_content,
             subject=f"Meeting Notes: {meeting_title}"
        )

        # Send email using Sendinblue API
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(f"Email sent successfully, details: {api_response}")
    except ApiException as e:
        print(f"Error sending email: {e}")
    except Exception as e:
          print(f"Error: {str(e)}")