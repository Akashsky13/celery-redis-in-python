from celery import Celery
from celery.schedules import crontab
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import sqlite3

app = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

# Celery Beat schedule configuration
app.conf.beat_schedule = {
    'send-monthly-report': {
        'task': 'tasks.send_monthly_report',
        'schedule': crontab(minute=0, hour=0, day_of_month=1),
,  # Run daily at midnight
    },
    'send-reminder': {
        'task': 'tasks.send_reminder',
        'schedule': 30.0,  # Run every 10 minutes
    },
}

app.conf.timezone = 'UTC'  # Or your preferred timezone

def send_email(to_email, subject, message, from_email='exapmle@gmail.com', password='your password'):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'html'))  # Changed to 'html' to support HTML content

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        return 'Email sent successfully'
    except Exception as e:
        return str(e)

def fetch_users_for_reminder():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    
    # Calculate the threshold time (24 hours ago from now)
    last_login_threshold = datetime.utcnow() - timedelta(hours=24)
    
    cursor.execute("""
        SELECT DISTINCT l.email
        FROM login l
        WHERE l.last_login < ?
    """, (last_login_threshold,))
    
    users_for_reminder = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    return users_for_reminder

def fetch_user_requests():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT l.email, r.book_name, r.author_name, r.request_date, r.status, r.issue_date
        FROM Requests r
        JOIN login l ON r.user_id = l.id
    """)
    user_requests = {}
    for row in cursor.fetchall():
        email = row[0]
        book_details = {
            'book_name': row[1],
            'author_name': row[2],
            'request_date': row[3],
            'status': row[4],
            'issue_date': row[5]
        }
        if email not in user_requests:
            user_requests[email] = []
        user_requests[email].append(book_details)
    conn.close()
    return user_requests

@app.task
def send_reminder():
    users_for_reminder = fetch_users_for_reminder()
    subject = 'We Miss You!'
    message = """
    <h1>We Miss You!</h1>
    <p>It's been more than 24 hours since you last logged in. Come back and check out what's new!</p>
    """
    for email in users_for_reminder:
        send_email(email, subject, message)

@app.task
def send_monthly_report():
    user_requests = fetch_user_requests()
    for email, requests in user_requests.items():
        subject = 'Monthly Report'
        message = '<h1>This is your monthly report.</h1>'
        for req in requests:
            message += f"""
            <p><strong>Book Name:</strong> {req['book_name']}</p>
            <p><strong>Author Name:</strong> {req['author_name']}</p>
            <p><strong>Request Date:</strong> {req['request_date']}</p>
            <p><strong>Status:</strong> {req['status']}</p>
            <p><strong>Issue Date:</strong> {req['issue_date']}</p>
            <hr>
            """
        send_email(email, subject, message)

# Ensure your Celery worker and beat services are running to test the task.
