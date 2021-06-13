import smtplib
def email(det):
    sender_email = "omar.ghanima06@gmail.com"
    rec_email = "brianjin84@gmail.com"
    password = "Passcode618"
    message = "One of your loved ones has collapsed, this may be due to a stroke or a heart-related issue. Medical assistance is on the way. Visit Orli, and use the password: obomt63 to track your loved one."

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("omar.ghanima06@gmail.com", password)
    print("It logged in")
    server.sendmail(sender_email, rec_email, message)
    print("Email has been sent to ", rec_email)
    