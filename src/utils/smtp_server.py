import smtplib
import ssl
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.utils.config import API_HOST, SENDER, SENDER_PASSWORD


class AccountVerified:
    def __inti__(self):
        self.sender = SENDER
        self.sender_password = SENDER_PASSWORD

    def build_email_template(fields: dict) -> str:
        html_template = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Verify Your Email Address</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        line-height: 1.6;
                        color: #333;
                        max-width: 600px;
                        margin: 0 auto;
                        padding: 20px;
                    }}
                    .button {{
                        display: inline-block;
                        padding: 12px 24px;
                        background-color: #4CAF50;
                        color: #ffffff;
                        text-decoration: none;
                        border-radius: 5px;
                        font-weight: bold;
                        font-size: 16px;
                        margin: 20px 0;
                    }}
                    .footer {{
                        margin-top: 20px;
                        font-size: 12px;
                        color: #666;
                    }}
                </style>
            </head>
            <body>
                <h1>Verify Your Email Address</h1>
                <p>Dear {user_name},</p>
                <p>Thank you for creating an account with {company_name}. We're excited to have you on board! To ensure the security of your account and to start using our services, we need to verify your email address.</p>
                <p>Please click the button below to confirm your email and activate your account:</p>
                <p>
                    <a href="{verification_url}" class="button">Verify My Email</a>
                </p>
                <p>If the button above doesn't work, you can also copy and paste the following link into your browser:</p>
                <p>{verification_url}</p>
                <p>This link will expire in {expiration_hours} hours for security reasons. If you don't verify your email within this time, you may need to request a new verification email.</p>
                <p>If you didn't create an account with {company_name}, please disregard this email. It's possible someone entered your email address by mistake.</p>
                <p>If you have any questions or need assistance, please don't hesitate to contact our support team at {support_email}.</p>
                <p>We look forward to seeing you on our platform!</p>
                <p>Best regards,<br>{company_name} Team</p>
                <div class="footer">
                    <p>This is an automated message, please do not reply directly to this email.</p>
                    <p>© {current_year} {company_name}. All rights reserved.</p>
                    <p>{company_address}</p>
                </div>
            </body>
            </html>
        """

        html_template = html_template.format(**fields)

    def send_email(self, user: dict):
        message = MIMEMultipart("alternative")
        message["Subject"] = "Verify Your Account"
        message["From"] = self.sender
        message["To"] = user.email

        # Prepare the data
        context = {
            "user_name": user.name,
            "company_name": "OY Management Company",
            "verification_url": f"{API_HOST}/verify_account?token={user.id}",
            "expiration_hours": 10,
            "support_email": "support@oy-management.com",
            "current_year": datetime.now().year,
            "company_address": "123 Main St, Amman",
        }

        html_template = self.build_email_template(context)

        page = MIMEText(html_template, "html")
        message.attach(page)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(self.sender, self.sender_password)
            server.sendmail(self.sender, user.email, message.as_string())
