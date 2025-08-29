from flask import Flask, render_template, request, url_for, flash, redirect
import os
from flask_mail import Mail, Message
from dotenv import load_dotenv


load_dotenv()


app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")


port = int(os.environ.get("PORT", 5000))

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = ''     # replace with your Gmail
app.config['MAIL_PASSWORD'] =  os.getenv("MAIL_PASSWORD")      # use App Password, not normal password
app.config['MAIL_DEFAULT_SENDER'] =  os.getenv("MAIL_USERNAME")

mail = Mail(app)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        try:
            msg = Message(
                subject=f"New message from {name}",
                recipients=[os.getenv("MAIL_RECIPIENT")],  # where you want to receive messages
                body=f"From: {name} <{email}>\n\n{message}"
            )
            mail.send(msg)
            flash("Message sent successfully!", "success")
        except Exception as e:
            flash(f"Error sending message: {e}", "danger")

        return redirect(url_for("contact"))

    return render_template("contact.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)