from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Set your email credentials
sender_email = "your_email@gmail.com"
sender_password = "your_password"
receiver_email = "boss_email@example.com"

# Set up the message
subject = "Request for Hike"
body = "Dear Boss,\n\nI hope this message finds you well. I wanted to discuss the possibility of a salary hike.\n\nBest regards,\nYour Name"

# Initialize the web driver
driver = webdriver.Chrome("path_to_chromedriver")

# Open the email service
driver.get("https://mail.example.com")  # replace with your email service

# Log in to your email
username_input = driver.find_element_by_name("username")  # replace with actual name of input field
password_input = driver.find_element_by_name("password")  # replace with actual name of input field
login_button = driver.find_element_by_id("login-button")  # replace with actual id of login button

username_input.send_keys(sender_email)
password_input.send_keys(sender_password)
login_button.click()

# Wait for the inbox to load
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'Inbox')]")))

# Send the email
new_email_button = driver.find_element_by_xpath("//button[contains(text(),'Compose')]")  # replace with actual text of compose button
new_email_button.click()

to_input = driver.find_element_by_name("to")  # replace with actual name of input field
subject_input = driver.find_element_by_name("subject")  # replace with actual name of input field
body_input = driver.find_element_by_xpath("//div[@role='textbox']")  # replace with actual xpath of the body input

to_input.send_keys(receiver_email)
subject_input.send_keys(subject)
body_input.send_keys(body)
body_input.send_keys(Keys.CONTROL + Keys.ENTER)

# Close the browser
driver.quit()

# Send an email using smtplib
def send_email():
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()

# Check if it's been 3 months since the last email
# Assuming last email was sent on 2023-07-24
last_email_date = datetime(2023, 7, 24)
current_date = datetime.now()
difference = current_date - last_email_date

if difference.days >= 90:  # 90 days is approximately 3 months
    send_email()
    print("Email sent successfully.")
else:
    print(f"It's been only {difference.days} days since the last email. Wait for {90 - difference.days} more days.")
