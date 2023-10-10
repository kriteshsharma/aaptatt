from flask import Flask, render_template, request, redirect, url_for
import pymysql
from config import Config  # Import the Config class

app = Flask(__name__)

# Configure your app using the Config class
app.config.from_object(Config)

# Create a PyMySQL database connection
mysql = pymysql.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    db=app.config['MYSQL_DB']
)
# Create a PyMySQL database connection
mysql = pymysql.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    db=app.config['MYSQL_DB']
)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = None
    error = None
    users = []

    if request.method == "POST":
        details = request.form
        firstName = details['fname']
        lastName = details['lname']
        cur = mysql.cursor()

        if not firstName.strip() or not lastName.strip():
            error = "First Name and Last Name cannot be empty."
        else:
            cur = mysql.cursor()
        # Check if the entry already exists
            cur.execute("SELECT * FROM myuserdata WHERE firstName = %s AND lastName = %s", (firstName, lastName))
            if cur.fetchone():
                error = f'Duplicate entry: {firstName} {lastName} already exists in the database.'
            else:
                cur.execute("INSERT INTO myuserdata(firstName, lastName) VALUES (%s, %s)", (firstName, lastName))
                mysql.commit()
                message = f'Successfully added {firstName} {lastName} to the database.'

            cur.close()

    # Fetch existing users from the database
    cur = mysql.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT firstName, lastName FROM myuserdata")
    users = cur.fetchall()
    print(users)
    cur.close()

    return render_template('index.html', message=message, error=error, users=users)

@app.route('/delete/<string:first_name>/<string:last_name>', methods=['POST'])
def delete_user(first_name, last_name):
    cur = mysql.cursor()
    cur.execute("DELETE FROM myuserdata WHERE firstName = %s AND lastName = %s", (first_name, last_name))
    mysql.commit()
    cur.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
