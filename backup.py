import os
import shutil
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import schedule
import time
from datetime import datetime

load_dotenv()

sender_mail = os.getenv('sender_mail')
app_password = os.getenv('app_password')
receiver_mail = os.getenv('receicer_mail')

source_folder = "./"         
backup_folder = "./backup/"

os.makedirs(backup_folder, exist_ok=True)

def send_email(subject, body):
    """Gửi email thông báo"""
    msg = MIMEMultipart()
    msg['From'] = sender_mail
    msg['To'] = receiver_mail
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_mail, app_password)
        server.send_message(msg)
        server.quit()
        print("Đã gửi email thành công.")
    except Exception as e:
        print(f"Gửi email thất bại: {e}")

def backup_database():
    """Backup database files"""
    try:
        files = os.listdir(source_folder)
        db_files = [f for f in files if f.endswith('.sql') or f.endswith('.sqlite3')]

        if not db_files:
            raise Exception("Không tìm thấy file database để backup.")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        for file_name in db_files:
            src = os.path.join(source_folder, file_name)
            dst = os.path.join(backup_folder, f"{timestamp}_{file_name}")
            shutil.copy2(src, dst)

        send_email(
            subject="Backup Database Thành Công",
            body=f"Đã backup thành công {len(db_files)} file database lúc {timestamp}."
        )
    except Exception as e:
        send_email(
            subject="Backup Database Thất Bại",
            body=f"Có lỗi xảy ra khi backup database: {e}")

schedule.every().day.at("00:00").do(backup_database)

print("Đang chạy lịch trình backup...")

while True:
    schedule.run_pending()
    time.sleep(60)
