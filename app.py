from flask import Flask, render_template, request, redirect, url_for, flash
import csv
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "change_this_to_a_secret"  # set via env var in production

CONTACTS_CSV = os.path.join(app.root_path, 'contacts.csv')

@app.route('/')
def index():
    projects = [
        {"title": "Project A", "desc": "Hospital based ", "url": "#"},
        {"title": "Project B", "desc": "Tourism based", "url": "#"}
    ]
    return render_template('index.html', projects=projects)

@app.route('/projects')
def projects():
    projects = [
        {"title": "Project A", "desc": "Hospital based", "url": "#"},
        {"title": "Project B", "desc": "Tourism based", "url": "#"}
    ]
    return render_template('projects.html', projects=projects)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()

        if not name or not email or not message:
            flash("Please fill all fields.", "error")
            return redirect(url_for('contact'))

        header_needed = not os.path.exists(CONTACTS_CSV)
        try:
            with open(CONTACTS_CSV, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                if header_needed:
                    writer.writerow(['timestamp_utc', 'name', 'email', 'message'])
                writer.writerow([datetime.utcnow().isoformat(), name, email, message])
            flash("Thanks — your message was received.", "success")
        except Exception:
            flash("Failed to save your message. Try again.", "error")
        return redirect(url_for('contact'))

    return render_template('contact.html')

# Optional: read contacts (dev only — remove or protect in production)
@app.route('/_contacts')
def _contacts():
    if not os.path.exists(CONTACTS_CSV):
        return "No contacts yet."
    with open(CONTACTS_CSV, 'r', encoding='utf-8') as f:
        return "<pre>" + f.read() + "</pre>"

if __name__ == '__main__':
    app.run(debug=True)
