import smtplib
from email.mime.text import MIMEText


def send_mail(customer, coffee, rating, comments):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = ''
    password = ''
    message = f"<h3>New Feedback!</h3><ul><li>Customer: {customer}</li><li>Coffee: {coffee}</li><li>Rating: {rating}</li><li>Comment: {comments}</li></ul>"
    
    sender_email = 'sender@demo.com'
    receiver_email = 'receiver@demo.com'
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'Coffee Feedback'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    #Send email
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        