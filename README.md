# Django_OTP_Twilio
An example of One-Time Password implementation for Django App using Twilio SMS gateway.

Need to install django-otp-twilio package.
For api reference doc visit http://pythonhosted.org/django-otp-twilio/ .

And also you need to signup and get the details for settings from https://www.twilio.com/try-twilio .
The following fields have to be filled up in settings.py file:
OTP_TWILIO_ACCOUNT = ''
OTP_TWILIO_AUTH = ''
OTP_TWILIO_FROM = ''