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
receiver_mail = os.getenv('receiver_mail') 

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
    try:
        if not os.path.exists(backup_folder):
            os.makedirs(backup_folder)

        files_backed_up = []
        now = datetime.now().strftime("%Y-%m-%d_%H-%M")

        for filename in os.listdir(source_folder):
            if filename.endswith(".sql") or filename.endswith(".sqlite3"):
                src_path = os.path.join(source_folder, filename)
                new_filename = f"{now}_{filename}"
                dest_path = os.path.join(backup_folder, new_filename)
                shutil.copy2(src_path, dest_path)
                files_backed_up.append(new_filename)

        if files_backed_up:
            subject = "Backup thành công"
            body = "Các file sau đã được backup thành công:\n" + "\n".join(files_backed_up)
        else:
            subject = "Backup hoàn tất - Không có file cần backup"
            body = "Không tìm thấy file .sql hoặc .sqlite3 nào để backup."

        send_email(subject, body)
    except Exception as e:
        subject = "Backup thất bại"
        body = f"Đã xảy ra lỗi trong quá trình backup:\n{e}"
        send_email(subject, body)


schedule.every().day.at("13:46").do(backup_database)

print("Đang chạy lịch trình backup...")

while True:
    schedule.run_pending()
    time.sleep(60)
