# import main flask dependencies
from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps
import mysql.connector
import hashlib
from flask_wtf.csrf import CSRFProtect, generate_csrf

# import for profile picture feature
import os
from werkzeug.utils import secure_filename

# import dependencies for PASSWORD RESET
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer

# CSRF Protection
csrf = CSRFProtect()

UPLOAD_FOLDER = 'static/uploads/profile_pics'  # Directory for profile pictures
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = 'my_secret_key'
app.config['WTF_CSRF_ENABLED'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


csrf.init_app(app)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'adet'
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Connection to database
def get_db_connection():
    conn = mysql.connector.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database']
    )
    return conn

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'clariskyco@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'mmap spkz bekp relj'  # Replace with your email password or app-specific password 
app.config['MAIL_DEFAULT_SENDER'] = 'clariskyco@gmail.com'

mail = Mail(app)

# Serializer for generating secure tokens
s = URLSafeTimedSerializer(app.secret_key)

# Generate Password Reset Token
def generate_reset_token(email):
    return s.dumps(email, salt='password-reset-salt')


# Function to Validate Token
def verify_reset_token(token, expiration=3600):
    try:
        email = s.loads(token, salt='password-reset-salt', max_age=expiration)
    except Exception as e:
        return None  # Return None if token is invalid or expired
    return email

# Verify Reset Token
def verify_reset_token(token, expiration=3600):
    try:
        email = s.loads(token, salt='password-reset-salt', max_age=expiration)
    except Exception as e:
        return None  # Return None if token is invalid or expired
    return email

# functools.wrap; protect from unauthorized access
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))  # Redirect to login if user is not authenticated
        return f(*args, **kwargs)
    return decorated_function

# wrapper for admin accounts
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'admin':
            return redirect(url_for('dashboard'))  # Redirect if not admin
        return f(*args, **kwargs)
    return decorated_function


# added a redirect for http://127.0.0.1:5000 to the login route
@app.route('/')
def home():
    return redirect(url_for('login'))

# Request Reset Password
@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if request.method == 'POST':
        email = request.form['email']
        
        # Check if the email exists in the database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM adet_user WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            # Generate a reset token
            token = generate_reset_token(email)

            # Send reset email
            reset_link = url_for('reset_password', token=token, _external=True)
            msg = Message('Password Reset Request', recipients=[email])
            msg.body = f'Click the following link to reset your password: {reset_link}'
            mail.send(msg)

            return render_template('reset_password_request.html', message="Check your email for the reset link.")

        return render_template('reset_password_request.html', error="Email not found.")

    return render_template('reset_password_request.html')

# Reset Password
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    email = verify_reset_token(token)
    if not email:
        return redirect(url_for('reset_password_request'))

    if request.method == 'POST':
        new_password = request.form['password']

        # Hash the new password
        hashed_password = hashlib.sha256(new_password.encode('utf-8')).hexdigest()

        # Update password in the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE adet_user SET password = %s WHERE email = %s', (hashed_password, email))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('login'))

    return render_template('reset_password.html', token=token)


# Login webpage routing
@app.route('/login', methods=['GET', 'POST'])
def login():
    csrf_token = generate_csrf()  # Generate CSRF token
    print(f"CSRF Token: {csrf_token}")
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM adet_user WHERE email = %s', (email,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        # Hash the provided password and compare with the stored hashed password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        if user and user['password'] == hashed_password:
            session['user_id'] = user['id']
            session['first_name'] = user['first_name']
            session['role'] = user['role']

            # Redirect admin to the admin dashboard, others to regular dashboard
            if user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid username or password")

    return render_template('login.html')

# Register webpage routing
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM adet_user WHERE email = %s', (email,))
        existing_user = cursor.fetchone()

        # existing user checker
        if existing_user:
            cursor.close()
            conn.close()
            return render_template('register.html', error="Email already exists.")

        # Use hashlib to hash the password
        password = request.form.get('password')
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        form_data = {
            "first_name": request.form.get('first_name'),
            "middle_name": request.form.get('middle_name'),
            "last_name": request.form.get('last_name'),
            "contact_number": request.form.get('contact_number'),
            "email": request.form.get('email'),
            "address": request.form.get('address'),
            "password": hashed_password
        }

        # insert data into database
        cursor.execute('''INSERT INTO adet_user (first_name, middle_name, last_name, contact_number, email, address, password, role)
                          VALUES (%s, %s, %s, %s, %s, %s, %s, 'user')''', 
                          (form_data['first_name'], form_data['middle_name'], form_data['last_name'], 
                           form_data['contact_number'], form_data['email'], form_data['address'],
                           form_data['password']))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('login'))

    return render_template('register.html')


# < =============== ADMIN ONLY =============== > #
# admin webpage routing // only admins can access the following webpages
@app.route('/admin/dashboard', methods=['GET'])
@login_required
@admin_required
def admin_dashboard():
    # Retrieve the role filter from query parameters (default is None for no filter)
    role_filter = request.args.get('role', default=None)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if role_filter:
        cursor.execute('SELECT * FROM adet_user WHERE role = %s ORDER BY first_name', (role_filter,))
    else:
        cursor.execute('SELECT * FROM adet_user ORDER BY first_name')

    users = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('admin_dashboard.html', users=users, role_filter=role_filter, enumerate=enumerate)

# add user routing // requires admin access
@app.route('/add_user', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    if request.method == 'POST':
        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        last_name = request.form['last_name']
        contact_number = request.form['contact_number']
        email = request.form['email']
        address = request.form['address']
        password = request.form['password']
        role = request.form['role']  # Capture the role

        # Add the user to the database (make sure to hash the password)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO adet_user (first_name, middle_name, last_name, contact_number, email, address, password, role) '
            'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
            (first_name, middle_name, last_name, contact_number, email, address, password, role)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('admin_dashboard'))

    return render_template('add_user.html')


# edit password routing
@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Retrieve the user information
    cursor.execute("SELECT * FROM adet_user WHERE id = %s", (user_id,))
    user = cursor.fetchone()

    if request.method == 'POST':
        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        last_name = request.form['last_name']
        contact_number = request.form['contact_number']
        email = request.form['email']
        address = request.form['address']
        password = request.form['password']
        role = request.form['role']
        profile_picture = request.files.get('profile_picture')  # Retrieve the uploaded profile picture

        # If password is provided, hash it using hashlib
        if password:
            hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        else:
            hashed_password = user['password']  # Keep the existing password if none is provided

        # Handle the profile picture upload if there is a new file
        if profile_picture and allowed_file(profile_picture.filename):
            # Secure the file name and save the image
            filename = secure_filename(profile_picture.filename)
            profile_picture.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Update the user's profile picture in the database
            cursor.execute('UPDATE adet_user SET profile_picture = %s WHERE id = %s', (filename, user_id))
        
        # Update other user information (excluding password and profile_picture)
        cursor.execute("""
            UPDATE adet_user 
            SET first_name = %s, middle_name = %s, last_name = %s, 
                contact_number = %s, email = %s, address = %s, 
                password = %s, role = %s
            WHERE id = %s
        """, (first_name, middle_name, last_name, contact_number, email, address, hashed_password, role, user_id))
        
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('admin_dashboard'))

    cursor.close()
    conn.close()

    return render_template('edit_user.html', user=user)

# Deletes an existing user
@app.route('/admin/delete_user/<int:user_id>')
@login_required
@admin_required
def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM adet_user WHERE id = %s', (user_id,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('admin_dashboard'))


# < =============== REGULAR USERS =============== > #
# Routing to dashboard for users
@app.route('/dashboard')
# calls login_required function
@login_required
def dashboard():
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT first_name, middle_name, last_name, contact_number, email, address, profile_picture FROM adet_user WHERE id = %s', (user_id,))
    user_details = cursor.fetchone()
    
    cursor.close()
    conn.close()

    return render_template('dashboard.html', user_details=user_details)

# editing of profile
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user_id = session['user_id']
    if request.method == 'POST':
        # Update user info
        new_data = {
            "first_name": request.form.get('first_name'),
            "last_name": request.form.get('last_name'),
            "contact_number": request.form.get('contact_number'),
            "address": request.form.get('address')
        }

        profile_picture = request.files.get('profile_picture')

        # craete directory folder if it doesn't exist
        upload_folder = app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        conn = get_db_connection()
        cursor = conn.cursor()

        # Handle profile picture upload
        if profile_picture and allowed_file(profile_picture.filename):
            filename = secure_filename(profile_picture.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            try:
                profile_picture.save(file_path)
                # Update the database with the filename only if the file saves successfully
                cursor.execute('UPDATE adet_user SET profile_picture = %s WHERE id = %s', (filename, user_id))
                conn.commit()
            except Exception as e:
                print(f"Error saving file: {e}")
                filename = 'default.png'


        # Update other profile details
        cursor.execute('''UPDATE adet_user SET first_name = %s, last_name = %s, contact_number = %s, address = %s 
                          WHERE id = %s''', 
                          (new_data['first_name'], new_data['last_name'], new_data['contact_number'], new_data['address'], user_id))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('dashboard'))

    # Fetch current user details
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM adet_user WHERE id = %s', (user_id,))
    user_details = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template('edit_profile.html', user=user_details)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# remove cache to avoid outdated information
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

if __name__ == '__main__':
    app.run(debug=True)
