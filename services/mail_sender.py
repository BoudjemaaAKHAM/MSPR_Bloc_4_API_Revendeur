import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


def send_email(target, img):
    """
    This function sends an email with an image attached
    :param target:
    :param img:
    :return:
    """
    with open(img, 'rb') as i:
        img_data = i.read()

    sender = "guillaume.gay.74@gmail.com"
    msg = MIMEMultipart()
    msg['Subject'] = "QR Code d'authentification"
    msg['From'] = sender
    msg['To'] = target
    text = MIMEText(
        "Bonjour, \n\nVeuillez trouver en pj votre QR Code d'authentification.\n\nCordialement, \n\nL'équipe de RevendeurAPI")
    msg.attach(text)
    image = MIMEImage(img_data, name=os.path.basename(img))
    msg.attach(image)

    os.remove(img)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, "cybkqequeqtxfyic")
    # server.set_debuglevel(1)
    server.sendmail(sender, target, msg.as_string())
    server.quit()

    print("Email sent to " + target)
