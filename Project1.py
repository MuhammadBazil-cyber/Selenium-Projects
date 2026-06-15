import os
import time
import smtplib
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.common.by import By

# Personal notes:
# Remember to use implicit or explicit wait concept at the end of project.

# Email configuration:-

# SMTP-simple mail transfer protocol
SMTP_server = "smtp.gmail.com"
SMTP_port = 587
Sender_email = ""
Sender_password = ""
Receiver_email = ""

# list to carry logs
report_logs = []

# the r here is representing the raw string, as \ is an escape character.
network_path = r"C:\Users\mbazil\Downloads\Selenium P1"
# creating an object for setting chrome options
chrome_options = webdriver.ChromeOptions()
# now creating a dict for storing the standard named prefrences
# for chromes internal settings consideration.
prefs = {
        "download.default_directory": network_path,
        "download.prompt_for_download": False,
        "credentials_enable_service": False,
        "profile.password_manager_leak_detection": False,
        "profile.password_manager_enabled": False
}
# now passing the prefs to internal settings through options object
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(10)
overall_status = "SUCCESS"
try:
        driver.get("https://the-internet.herokuapp.com/login")
        # time.sleep(2)
        driver.find_element(By.ID, "username").send_keys("tomsmith")
        # time.sleep(2)
        driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
        # time.sleep(2)
        driver.find_element(By.CLASS_NAME, "radius").click()
        report_logs.append("✅ Step 1: Successfully logged in")
        time.sleep(2)
        driver.get("https://the-internet.herokuapp.com/download")
        driver.find_element(By.CSS_SELECTOR, "a[href='download/some-file.txt']").click()
        report_logs.append("✅ Step 2: Successfully downloaded the file")
        time.sleep(5)
        driver.get("https://the-internet.herokuapp.com/upload")
        # os.path.join() is an intelligent mini-machine.
        # It looks at what operating system your script is running on and
        # automatically pieces the folder path and file name together using
        # the mathematically perfect slashes.
        # It completely eliminates path formatting bugs.
        file = os.path.join(network_path, "some-file.txt")
        driver.find_element(By.ID, "file-upload").send_keys(file)
        driver.find_element(By.ID, "file-submit").click()
        report_logs.append("✅ Step 3: Successfully uploaded the file")
        print("Web steps executed successfully!")
except Exception as e:
        report_logs.append(f"❌ ERROR: Script crashed. Reason: {e}")
        print("Script hit an error! Check your email report.")
finally:
        body = "\n".join(report_logs)
        msg = MIMEText(body)
        msg["Subject"] = f"My Project Report: {overall_status}"
        msg["From"] = Sender_email
        msg["To"] = Receiver_email

        server = smtplib.SMTP(SMTP_server, SMTP_port)
        server.starttls()
        server.login(Sender_email, Sender_password)
        server.sendmail(Sender_email, Receiver_email, msg.as_string())
        server.quit()
        driver.quit()
