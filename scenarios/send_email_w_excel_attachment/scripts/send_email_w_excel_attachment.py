#scripts/send_email_w_excel_attachment.py
import os
import sys
os.system(f"{sys.executable} -m pip install openpyxl")

import pandas as pd
import pytd
from io import BytesIO
import smtplib
from email.message import EmailMessage
from email.utils import formataddr

def main(**kwargs):
  # Init
  td_api_key = os.getenv("TD_API_KEY")
  td_api_ep = os.getenv("TD_API_EP")
  gmail_app_pw = os.getenv("GMAIL_APP_PW")
  database = os.getenv("DATABASE")
  src_tbl = os.getenv("SRC_TBL")
  sender_email = os.getenv("SENDER_EMAIL")
  sender_name = os.getenv("SENDER_NAME")

  td = pytd.Client(apikey=td_api_key, endpoint=td_api_ep, database=database, default_engine="presto")
  # Create a dataframe by importing data from Activation Actions database.table
  data_res = td.query(f"SELECT * FROM TABLE(exclude_columns(input => TABLE({database}.{src_tbl}),columns => DESCRIPTOR(email_to,email_subject)))")
  data_df = pd.DataFrame(**data_res)
  email_to_res = td.query(f"SELECT email_to FROM {database}.{src_tbl} LIMIT 1")
  email_to_df = pd.DataFrame(**email_to_res)
  email_to = email_to_df.squeeze()
  email_subject_res = td.query(f"SELECT email_subject FROM {database}.{src_tbl} LIMIT 1")
  email_subject_df = pd.DataFrame(**email_subject_res)
  email_subject = email_subject_df.squeeze()

  # Save the dataframe to an excel file in memory
  excel_buffer = BytesIO()
  data_df.to_excel(excel_buffer, index=False, sheet_name="Scores")
  excel_buffer.seek(0)

  # Prepare the email
  msg = EmailMessage()
  msg["Subject"] = email_subject
  msg["From"] = formataddr((sender_name, sender_email))
  msg["To"] = email_to
  msg.set_content("Hi,\n\nPlease find the attached excel file.\n\nBest regards,\nTD CDP Sony SG")
  msg.add_attachment(
      excel_buffer.read(),
      maintype="application",
      subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      filename="report.xlsx"
  )

  # Send the email with Gmail SMTP
  smtp_server = "smtp.gmail.com"
  smtp_port = 587
  smtp_account = "your_gmail_account@treasure-data.com"
  password = gmail_app_pw  # generate app password: https://myaccount.google.com/apppasswords

  with smtplib.SMTP(smtp_server, smtp_port) as server:
      server.starttls()
      server.login(smtp_account, password)
      server.send_message(msg)

  print("Email sent successfully!")
  print(msg)

# Main
if __name__ == "__main__":
  main()
