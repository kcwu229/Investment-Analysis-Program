from flask import Flask
from flask import render_template, request
from flask_mail import Mail, Message
import emailConfig
import datetime

app = Flask(__name__)
app.config['MAIL_SERVER'] = emailConfig.mailSever
app.config['MAIL_PORT'] = emailConfig.mailPort
app.config['MAIL_USERNAME'] = emailConfig.mailUsername
app.config['MAIL_PASSWORD'] = emailConfig.mailPassword
app.config['MAIL_USE_TLS'] = emailConfig.mailTLS
app.config['MAIL_USE_SSL'] = emailConfig.mailSSL
mail = Mail(app)

systemYear = datetime.date.today().year
#LandingPage && Sending Subscription Email Function
@app.route("/", methods=['GET', 'POST'])
def index():    
    # Send Subscription email 
    if request.method == 'POST':
        msg_title = 'BetaStock -- Subscription Anouncement'
        msg_sender = emailConfig.mailUsername
        msg_recipients = [f'{request.values["emailField"]}']    
        msg = Message(msg_title, sender=msg_sender, recipients=msg_recipients)
        msg.html = render_template('aa.html', **locals())
        mail.send(msg)
    return render_template("landPage.html", systemYear=systemYear)

#SignInPage
@app.route("/signIn")
def signIn():     
    # how to import background image url in flask ?
    return render_template("login.html")

#SignUp Page
@app.route("/signUp")
def signUp():     
    questionList = ["What is your date of birth?", 
                    "What was your favorite school teacher’s name?", 
                    "What’s your favorite movie?", 
                    "What was your first car?",
                    "What city were you born in?"]    
    return render_template("signUp.html", questionList=questionList)

#Redirect to Completion Page/ or wait 3 seconds then back to signInPage After registration
# -- may need to set conditions
@app.route("/registSuccess", methods=['POST'])
def registSuccess():
    # store to DataBase for user table
    username = request.values['username']
    password = request.values['password']
    displayName = request.values['displayName']
    email = request.values['email']
    # SEND HTML EMAIL -- displayName, username && password
    msg_title = 'BetaStock Confirmation Email'
    msg_sender = emailConfig.mailUsername
    msg_recipients = [f'{email}'] 
    msg = Message(msg_title, sender=msg_sender, recipients=msg_recipients)

    # Keep tidy in HTML display format, make following rules:
    # Display length of uername: 9, password: 7 (Normal display in first 2 words and display * for the remaining)
    displayUsername = username[0:10]
    password = f"{password[0:2]}*****"
    msg.html = render_template('ConfirmationEmail.html', displayName=displayName, username=displayUsername, password=password, systemYear=systemYear)
    mail.send(msg)
    return render_template('signUp.html')

#FunctionPage
@app.route("/keyScreen", methods=['POST'])
def keyScreen():
    username = request.values['username']
    password = request.values['password']
    # Check with Database e.g. MYSQL
    return render_template("keyScreen.html", **locals())

if __name__ == "__main__":
    app.run(debug=True)