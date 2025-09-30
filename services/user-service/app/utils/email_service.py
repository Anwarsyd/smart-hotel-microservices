# # app/utils/email_service.py
# import smtplib
# import os
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from dotenv import load_dotenv
# import logging

# load_dotenv()

# logger = logging.getLogger(__name__)

# # Email configuration from environment variables
# SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
# SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
# SMTP_USER = os.getenv("SMTP_USER")
# SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
# FROM_EMAIL = os.getenv("FROM_EMAIL", SMTP_USER)
# BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")


# def send_verification_email(to_email: str, username: str, token: str) -> bool:
#     """
#     Send verification email to user
    
#     Args:
#         to_email: Recipient email address
#         username: User's username
#         token: Verification token
        
#     Returns:
#         bool: True if email sent successfully, False otherwise
#     """
#     try:
#         # Create verification link
#         verification_link = f"{BASE_URL}/auth/verify?token={token}"
        
#         # Create message
#         msg = MIMEMultipart('alternative')
#         msg['Subject'] = "Verify Your Smart Hotel Account"
#         msg['From'] = FROM_EMAIL
#         msg['To'] = to_email
        
#         # Plain text version
#         text = f"""
# Hello {username},

# Thank you for registering with Smart Hotel!

# Please verify your email address by clicking the link below:
# {verification_link}

# This link will expire in 24 hours.

# If you didn't create this account, please ignore this email.

# Best regards,
# Smart Hotel Team
#         """
        
#         # HTML version
#         html = f"""
# <!DOCTYPE html>
# <html>
# <head>
#     <style>
#         body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
#         .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
#         .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
#         .content {{ padding: 20px; background-color: #f9f9f9; }}
#         .button {{ 
#             display: inline-block; 
#             padding: 12px 30px; 
#             background-color: #4CAF50; 
#             color: white; 
#             text-decoration: none; 
#             border-radius: 5px;
#             margin: 20px 0;
#         }}
#         .footer {{ padding: 20px; text-align: center; font-size: 12px; color: #777; }}
#     </style>
# </head>
# <body>
#     <div class="container">
#         <div class="header">
#             <h1>Welcome to Smart Hotel!</h1>
#         </div>
#         <div class="content">
#             <h2>Hello {username},</h2>
#             <p>Thank you for registering with Smart Hotel!</p>
#             <p>Please verify your email address by clicking the button below:</p>
#             <p style="text-align: center;">
#                 <a href="{verification_link}" class="button">Verify Email Address</a>
#             </p>
#             <p>Or copy and paste this link into your browser:</p>
#             <p style="word-break: break-all; color: #4CAF50;">{verification_link}</p>
#             <p><strong>This link will expire in 24 hours.</strong></p>
#             <p>If you didn't create this account, please ignore this email.</p>
#         </div>
#         <div class="footer">
#             <p>© 2025 Smart Hotel. All rights reserved.</p>
#         </div>
#     </div>
# </body>
# </html>
#         """
        
#         # Attach both versions
#         part1 = MIMEText(text, 'plain')
#         part2 = MIMEText(html, 'html')
#         msg.attach(part1)
#         msg.attach(part2)
        
#         # Send email
#         with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
#             server.starttls()
#             server.login(SMTP_USER, SMTP_PASSWORD)
#             server.sendmail(FROM_EMAIL, [to_email], msg.as_string())
        
#         logger.info(f"Verification email sent successfully to {to_email}")
#         return True
        
#     except Exception as e:
#         logger.error(f"Failed to send verification email to {to_email}: {str(e)}")
#         return False


# def send_welcome_email(to_email: str, username: str) -> bool:
#     """
#     Send welcome email after successful verification
    
#     Args:
#         to_email: Recipient email address
#         username: User's username
        
#     Returns:
#         bool: True if email sent successfully, False otherwise
#     """
#     try:
#         msg = MIMEMultipart('alternative')
#         msg['Subject'] = "Welcome to Smart Hotel!"
#         msg['From'] = FROM_EMAIL
#         msg['To'] = to_email
        
#         text = f"""
# Hello {username},

# Your email has been verified successfully!

# You can now login and enjoy all the features of Smart Hotel.

# Best regards,
# Smart Hotel Team
#         """
        
#         html = f"""
# <!DOCTYPE html>
# <html>
# <head>
#     <style>
#         body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
#         .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
#         .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
#         .content {{ padding: 20px; background-color: #f9f9f9; }}
#         .footer {{ padding: 20px; text-align: center; font-size: 12px; color: #777; }}
#     </style>
# </head>
# <body>
#     <div class="container">
#         <div class="header">
#             <h1>✅ Email Verified!</h1>
#         </div>
#         <div class="content">
#             <h2>Hello {username},</h2>
#             <p>Congratulations! Your email has been verified successfully.</p>
#             <p>You can now login and explore all the amazing features Smart Hotel has to offer.</p>
#             <p>Happy booking!</p>
#         </div>
#         <div class="footer">
#             <p>© 2025 Smart Hotel. All rights reserved.</p>
#         </div>
#     </div>
# </body>
# </html>
#         """
        
#         part1 = MIMEText(text, 'plain')
#         part2 = MIMEText(html, 'html')
#         msg.attach(part1)
#         msg.attach(part2)
        
#         with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
#             server.starttls()
#             server.login(SMTP_USER, SMTP_PASSWORD)
#             server.sendmail(FROM_EMAIL, [to_email], msg.as_string())
        
#         logger.info(f"Welcome email sent successfully to {to_email}")
#         return True
        
#     except Exception as e:
#         logger.error(f"Failed to send welcome email to {to_email}: {str(e)}")
#         return False


##

# app/utils/email_service.py
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

# Email configuration from environment variables
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
FROM_EMAIL = os.getenv("FROM_EMAIL", SMTP_USER)
BASE_URL = os.getenv("BASE_URL", "http://localhost:8001")

# Add this flag to enable/disable actual email sending
ENABLE_EMAIL = os.getenv("ENABLE_EMAIL", "false").lower() == "true"


def send_verification_email(to_email: str, username: str, token: str) -> bool:
    """
    Send verification email to user
    
    Args:
        to_email: Recipient email address
        username: User's username
        token: Verification token
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    
    # Create verification link
    verification_link = f"{BASE_URL}/auth/verify?token={token}"
    
    # If email is disabled, just print the link to console
    if not ENABLE_EMAIL:
        print("\n" + "="*70)
        print("📧 VERIFICATION EMAIL (Development Mode)")
        print("="*70)
        print(f"To: {to_email}")
        print(f"Username: {username}")
        print(f"Verification Link: {verification_link}")
        print("="*70 + "\n")
        
        logger.info(f"[DEV MODE] Verification link for {to_email}: {verification_link}")
        return True
    
    # Real email sending code (only runs if ENABLE_EMAIL=true)
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Verify Your Smart Hotel Account"
        msg['From'] = FROM_EMAIL
        msg['To'] = to_email
        
        # Plain text version
        text = f"""
Hello {username},

Thank you for registering with Smart Hotel!

Please verify your email address by clicking the link below:
{verification_link}

This link will expire in 24 hours.

If you didn't create this account, please ignore this email.

Best regards,
Smart Hotel Team
        """
        
        # HTML version
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
        .content {{ padding: 20px; background-color: #f9f9f9; }}
        .button {{ 
            display: inline-block; 
            padding: 12px 30px; 
            background-color: #4CAF50; 
            color: white; 
            text-decoration: none; 
            border-radius: 5px;
            margin: 20px 0;
        }}
        .footer {{ padding: 20px; text-align: center; font-size: 12px; color: #777; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Welcome to Smart Hotel!</h1>
        </div>
        <div class="content">
            <h2>Hello {username},</h2>
            <p>Thank you for registering with Smart Hotel!</p>
            <p>Please verify your email address by clicking the button below:</p>
            <p style="text-align: center;">
                <a href="{verification_link}" class="button">Verify Email Address</a>
            </p>
            <p>Or copy and paste this link into your browser:</p>
            <p style="word-break: break-all; color: #4CAF50;">{verification_link}</p>
            <p><strong>This link will expire in 24 hours.</strong></p>
            <p>If you didn't create this account, please ignore this email.</p>
        </div>
        <div class="footer">
            <p>© 2025 Smart Hotel. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
        """
        
        # Attach both versions
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2)
        
        # Send email
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(FROM_EMAIL, [to_email], msg.as_string())
        
        logger.info(f"Verification email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send verification email to {to_email}: {str(e)}")
        return False


def send_welcome_email(to_email: str, username: str) -> bool:
    """
    Send welcome email after successful verification
    
    Args:
        to_email: Recipient email address
        username: User's username
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    
    # If email is disabled, just print to console
    if not ENABLE_EMAIL:
        print("\n" + "="*70)
        print("🎉 WELCOME EMAIL (Development Mode)")
        print("="*70)
        print(f"To: {to_email}")
        print(f"Username: {username}")
        print("Message: Email verified successfully! Welcome to Smart Hotel!")
        print("="*70 + "\n")
        
        logger.info(f"[DEV MODE] Welcome email for {to_email}")
        return True
    
    # Real email sending code
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Welcome to Smart Hotel!"
        msg['From'] = FROM_EMAIL
        msg['To'] = to_email
        
        text = f"""
Hello {username},

Your email has been verified successfully!

You can now login and enjoy all the features of Smart Hotel.

Best regards,
Smart Hotel Team
        """
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
        .content {{ padding: 20px; background-color: #f9f9f9; }}
        .footer {{ padding: 20px; text-align: center; font-size: 12px; color: #777; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>✅ Email Verified!</h1>
        </div>
        <div class="content">
            <h2>Hello {username},</h2>
            <p>Congratulations! Your email has been verified successfully.</p>
            <p>You can now login and explore all the amazing features Smart Hotel has to offer.</p>
            <p>Happy booking!</p>
        </div>
        <div class="footer">
            <p>© 2025 Smart Hotel. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
        """
        
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2)
        
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(FROM_EMAIL, [to_email], msg.as_string())
        
        logger.info(f"Welcome email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send welcome email to {to_email}: {str(e)}")
        return False