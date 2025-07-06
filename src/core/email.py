import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import HTTPException
from src.config.env_vars import SMTP_PASSWORD, SMTP_SENDER_EMAIL, SMTP_PORT, SMTP_SERVER
import logging


def send_verification_email(email: str, otp_code: str):
    if not SMTP_SENDER_EMAIL or not SMTP_PASSWORD:
        logging.error("Email server configuration not set")
        raise HTTPException(
            status_code=500, detail="Email server configuration not set"
        )

    sender_email = SMTP_SENDER_EMAIL
    receiver_email = email
    smtp_server = SMTP_SERVER
    smtp_port = int(SMTP_PORT)
    password = SMTP_PASSWORD

    logging.info(f"Sending verification email to {email}")

    # Create the plain-text and HTML version of your message
    text = f"""
    Hi,

    Please verify your email by entering this 6 digit code: {otp_code}

    Thank you!
    """

    html = f"""
    <html>
    <body>
        <p>Hi,</p>
        <p>Please verify your email by entering this 6 digit code:</p>
        <h2>{otp_code}</h2>
        <p>Thank you!</p>
    </body>
    </html>
    """

    # Create a MIMEMultipart message
    message = MIMEMultipart("alternative")
    message["Subject"] = "Verify your email"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Attach both plain-text and HTML parts to the message
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)
    assert smtp_port
    assert smtp_server
    print(smtp_port,smtp_server)
    try:
        print("----------------------------")
        logging.info("Connecting to SMTP server...")
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            logging.info("Logging in to SMTP server...")
            server.login(sender_email, password)
            logging.info("Sending email...")
            server.sendmail(sender_email, receiver_email, message.as_string())
            logging.info("Email sent successfully")
    except smtplib.SMTPException as e:
        logging.error(f"Failed to send verification email: {str(e)}")
        raise e
        raise HTTPException(status_code=500, detail="Failed to send verification email")
