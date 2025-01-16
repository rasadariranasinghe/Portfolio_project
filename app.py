from flask import Flask, render_template, send_from_directory, request, redirect, url_for, flash
import requests
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# GitHub API URL
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")  # Use environment variable for GitHub username
GITHUB_API_URL = f"https://api.github.com/users/{GITHUB_USERNAME}/repos"

# Define the path where your resume PDF is stored
RESUME_FOLDER = os.path.join(app.root_path, 'static', 'resume')  # Ensure 'resume' folder is under 'static'

# Configure Flask app
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")  # Use environment variable for the secret key

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

    except requests.exceptions.RequestException as e:
        flash(f"Error fetching projects: {e}", "error")
        return render_template("projects.html", repos=[])

@app.route("/resume")
def resume():
    return render_template("resume.html")

@app.route("/contact", methods=["GET"])
def contact():
    # Render the contact page with email and GitHub links
    email = "your_email@example.com"
    github = "https://github.com/your_username"
    return render_template("contact.html", email=email, github=github)

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


if __name__ == "__main__":
    # Ensure that the app starts correctly
    print("Starting Flask app...")
    app.run(debug=True)
