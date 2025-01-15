from flask import Flask, render_template, send_from_directory, request, redirect, url_for, flash
import requests
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# GitHub API URL
GITHUB_USERNAME = "rasadariranasinghe"  # Replace with your GitHub username
GITHUB_API_URL = f"https://api.github.com/users/{GITHUB_USERNAME}/repos"

# Define the path where your resume PDF is stored
RESUME_FOLDER = os.path.join(app.root_path, 'static', 'resume')  # Ensure 'resume' folder is under 'static'

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/projects")
def projects():
    try:
        response = requests.get(GITHUB_API_URL)
        repos = response.json()
        if response.status_code != 200:
            flash("Error fetching GitHub repositories. Please try again later.", "error")
            return render_template("projects.html", repos=[])
        return render_template("projects.html", repos=repos)
    except Exception as e:
        flash(f"Error fetching projects: {e}", "error")
        return render_template("projects.html", repos=[])

@app.route("/resume")
def resume():
    return render_template("resume.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        # Extract form data
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        # Send email
        try:
            send_email(name, email, message)
            flash("Your message has been sent successfully!", "success")
            return redirect(url_for('thank_you'))
        except Exception as e:
            flash(f"Error sending your message: {e}", 'error')
            return redirect(url_for('contact'))

    return render_template("contact.html")

@app.route("/download_resume")
def download_resume():
    try:
        return send_from_directory(RESUME_FOLDER, "Rasadari_Ranasinghe_Resume.pdf")  # Serve the resume PDF for download
    except Exception as e:
        flash(f"Error downloading resume: {e}", 'error')
        return redirect(url_for('home'))

@app.route("/thank-you")
def thank_you():
    return render_template("thank_you.html")

def send_email(name, email, message):
    sender_email = "rasadariranasinghework@yahoo.com"  # Replace with your email
    receiver_email = "rasadariranasinghework@yahoo.com"  # Replace with your email (or a different one if needed)
    subject = f"Message from {name} ({email})"
    body = f"Message:\n\n{message}"
    
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, "plain"))
    
    try:
        with smtplib.SMTP_SSL('smtp.mail.yahoo.com', 465) as server:
            server.login(sender_email, 'RASADARIwork@96')  # Replace with your email password
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("Email sent successfully!")
    except Exception as e:
        raise Exception(f"Error sending email: {e}")

if __name__ == "__main__":
    # Ensure that the app starts correctly
    print("Starting Flask app...")
    app.run(debug=True)
