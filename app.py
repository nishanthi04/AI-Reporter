from flask import Flask, request, render_template, send_from_directory, redirect, url_for, flash, session
import os
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
import tensorflow as tf

# Load .env
load_dotenv()

# TensorFlow settings
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

# Custom modules
from modules.ocr_module import extract_text_from_image, extract_text_from_images
from modules.summarization_module import summarize_text, summarize_texts
from modules.formatter_module import format_as_news_report
from modules.text_to_speech_module import text_to_speech

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "fallback-key")

# Define paths
DATASET_PATH = "dataset/images"
UPLOADS_PATH = "uploads"
AUDIO_OUTPUT_PATH = "audio_reports"

# Flask-Login setup
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# In-memory user store
users = {
    'admin': {
        'password': generate_password_hash('admin123')
    }
}

# User class
class User(UserMixin):
    def __init__(self, username):
        self.id = username
        self.password = users[username]['password']

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id)
    return None

@app.route("/", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        if "newspaper_image" in request.files:
            image = request.files["newspaper_image"]
            image_path = os.path.join(UPLOADS_PATH, image.filename)
            image.save(image_path)

            extracted_text = extract_text_from_image(image_path)
            summary = summarize_text(extracted_text)
            audio_filename = os.path.join(UPLOADS_PATH, f"{os.path.splitext(image.filename)[0]}.mp3")
            text_to_speech(summary, output_filename=audio_filename)

            return render_template("index.html", report=summary, audio_file=f"/uploads/{os.path.basename(audio_filename)}")

    return render_template("index.html")

@app.route("/process_dataset", methods=["GET"])
@login_required
def process_dataset():
    if not os.path.exists(DATASET_PATH):
        return "Dataset folder does not exist. Please add images to 'dataset/images'.", 404

    extracted_texts = extract_text_from_images(DATASET_PATH)
    summarized_texts = summarize_texts(extracted_texts)
    formatted_reports = {img: format_as_news_report(summary) for img, summary in summarized_texts.items()}

    os.makedirs(AUDIO_OUTPUT_PATH, exist_ok=True)
    for image_name, report in formatted_reports.items():
        audio_filename = os.path.join(AUDIO_OUTPUT_PATH, f"{os.path.splitext(image_name)[0]}.mp3")
        text_to_speech(report, output_filename=audio_filename)

    return render_template("dataset_results.html", results=formatted_reports, audio_folder=AUDIO_OUTPUT_PATH)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOADS_PATH, filename)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        if uname in users and check_password_hash(users[uname]['password'], pwd):
            login_user(User(uname))
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Invalid username or password.")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        dob = request.form['dob']
        gender = request.form['gender']

        if uname in users:
            return render_template('register.html', error="Username already exists.")

        # Store user details
        users[uname] = {
            'password': generate_password_hash(pwd),
            'dob': dob,
            'gender': gender
        }

        # Auto login after registration
        login_user(User(uname))
        flash("Successfully Registered!", "success")
        return redirect(url_for('home'))  # 👈 redirect directly to AI News Reporter

    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# 🔧 Edit Profile Route
@app.route("/edit-profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    if request.method == "POST":
        new_username = request.form["username"]

        # Update user info
        users[new_username] = users.pop(current_user.id)
        current_user.id = new_username  # works for session
        flash("Profile updated!", "success")
        return redirect(url_for("home"))
    return render_template("edit_profile.html", username=current_user.id)

# 🔒 Change Password Route
@app.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        current_pwd = request.form["current_password"]
        new_pwd = request.form["new_password"]
        confirm_pwd = request.form["confirm_password"]

        # Verify current password
        if not check_password_hash(users[current_user.id]['password'], current_pwd):
            flash("Current password is incorrect.", "error")
        elif new_pwd != confirm_pwd:
            flash("New passwords do not match.", "error")
        else:
            users[current_user.id]['password'] = generate_password_hash(new_pwd)
            flash("Password changed successfully!", "success")
            return redirect(url_for("home"))
    return render_template("change_password.html")

# 🌗 Optional: Theme preference (if needed to store server-side)
@app.route("/set-theme/<mode>")
def set_theme(mode):
    session["theme"] = mode
    return redirect(request.referrer or url_for("home"))

if __name__ == "__main__":
    os.makedirs(UPLOADS_PATH, exist_ok=True)
    if not os.path.exists(DATASET_PATH):
        os.makedirs(DATASET_PATH)
    os.makedirs(AUDIO_OUTPUT_PATH, exist_ok=True)
    app.run(debug=True)
