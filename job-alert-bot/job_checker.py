import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ------------------------------------
# 🔗 STEP 1: Career Page URLs
# ------------------------------------
COMPANY_LINKS = {
    "NVIDIA": "https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite?locationHierarchy1=2fcb99c455831013ea52b82135ba3266",
    "Intel": "https://intel.wd1.myworkdayjobs.com/External"
}

# ------------------------------------
# 🧩 STEP 2: Keywords to Filter Jobs
# ------------------------------------
KEYWORDS = ["verification", "UVM", "AXI", "SystemVerilog", "AHB", "hardware"]

# ------------------------------------
# 📧 STEP 3: Email Configuration
# ------------------------------------
RECIPIENT_EMAIL = "djsatle2810@gmail.com"        # Your Gmail ID
SENDER_EMAIL = "djsatle2810@gmail.com"           # Same as sender here
APP_PASSWORD = "your-app-password-here"          # Gmail App Password (not regular password!)

# ------------------------------------
# 🔍 STEP 4: Scraping & Filtering
# ------------------------------------
def check_jobs():
    matching_jobs = []

    for company, url in COMPANY_LINKS.items():
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            elements = soup.find_all(['a', 'h2', 'h3'], string=True)
            for el in elements:
                title = el.text.strip().lower()
                if any(keyword.lower() in title for keyword in KEYWORDS):
                    matching_jobs.append(f"{company} → {title}")

        except Exception as e:
            print(f"Error processing {company}: {e}")

    return matching_jobs

# ------------------------------------
# 📬 STEP 5: Send Email
# ------------------------------------
def send_email(jobs):
    if not jobs:
        print("No matching jobs found.")
        return

    subject = "New_openings"
    body = "Hi Divyam,\n\nHere are new job postings:\n\n" + "\n".join(jobs) + "\n\nGood luck!\n— Copilot"

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

# ------------------------------------
# 🚀 STEP 6: Execute
# ------------------------------------
if __name__ == "__main__":
    jobs = check_jobs()
    send_email(jobs)
