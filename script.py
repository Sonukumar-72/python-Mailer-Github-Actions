import smtplib
from email.mime.text import MIMEText  # Handles the text of the email
from email.mime.multipart import MIMEMultipart  # Handles the structure of the email
import os

def send_mail(workflow_name, repo_name, workflow_run_id):
    # Email details
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    receiver_email = os.getenv('RECEIVER_EMAIL')

    # Email message
    subject = f"Workflow {workflow_name} failed for repo {repo_name}"
    body = f"""Hi,

The workflow {workflow_name} failed for the repo {repo_name}. Please check the logs for more details.

More Details:
Run_ID: {workflow_run_id}
"""

    # Construct the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Set up the server and send the email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()

        print('Email sent successfully')
    except Exception as e:
        print(f'Error: {e}')

# Call the function with environment variables
send_mail(os.getenv('WORKFLOW_NAME'), os.getenv('REPO_NAME'), os.getenv('WORKFLOW_RUN_ID'))
