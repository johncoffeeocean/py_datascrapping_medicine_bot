import smtplib

# Login credentials
email = 'hiroyamamoto918@gmail.com'
password = '1912010918'

# Email details
recipient = 'coffeeocecan918@gmail.com'
subject = 'Test Email'
body = 'This is a test email sent using Python!'

# Create message
message = f'Subject: {subject}\n\n{body}'

# Send email
with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    smtp.starttls()
    smtp.login(email, password)
    smtp.sendmail(email, recipient, message)