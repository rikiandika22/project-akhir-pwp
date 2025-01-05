from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from config.db_config import init_db
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = "12345"
mysql = init_db(app)

@app.route('/')
def index():
    if 'id_user' not in session:
        return redirect(url_for('login'))

    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT id, username, email, role FROM user")
        users = cur.fetchall()
        cur.close()
        return render_template('index.html', users=users)
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        role = request.form['role']
        password = request.form['password']

        hashed_password = generate_password_hash(password)

        try:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            
            # Periksa apakah username atau email sudah digunakan
            cur.execute("SELECT * FROM user WHERE username = %s OR email = %s", (username, email))
            existing_user = cur.fetchone()

            if existing_user:
                if existing_user['username'] == username:
                    flash('Username is already taken!', 'danger')
                elif existing_user['email'] == email:
                    flash('Email is already registered!', 'danger')
                return redirect(url_for('register'))

            # Jika tidak ada, tambahkan pengguna baru
            cur.execute("INSERT INTO user (username, email, role, password_hash) VALUES (%s, %s, %s, %s)", 
                        (username, email, role, hashed_password))
            mysql.connection.commit()
            cur.close()

            flash('Registration successful!', 'success')
            return redirect(url_for('login'))

        except Exception as e:
            flash(f"Error: {e}", 'danger')
            return redirect(url_for('register'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT id, username, email, password_hash FROM user WHERE email = %s", [email])
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user['password_hash'], password):
            session['id_user'] = user['id']
            session['username'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password!', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if 'id_user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        role = request.form['role']
        password = request.form['password']

        hashed_password = generate_password_hash(password)

        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO user (username, email, role, password_hash) VALUES (%s, %s, %s, %s)", 
                        (username, email, role, hashed_password))
            mysql.connection.commit()
            cur.close()
            flash('User added successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f"Error: {e}", 'danger')
    return render_template('add_user.html')

@app.route('/update_user/<int:id>', methods=['GET', 'POST'])
def update_user(id):
    if request.method == 'GET':  # Menangani GET untuk form edit
        try:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("SELECT id, username, email, role FROM user WHERE id = %s", [id])
            user = cur.fetchone()
            cur.close()

            if not user:
                flash('User not found.', 'danger')
                return redirect(url_for('index'))

            return render_template('edit_user.html', user=user)
        except Exception as e:
            flash(f'Terjadi kesalahan: {e}', 'danger')
            return redirect(url_for('index'))

    # Logika POST untuk update
    username = request.form['username']
    email = request.form['email']
    role = request.form['role']
    password = request.form.get('password', None)

    try:
        cur = mysql.connection.cursor()
        if password:  # Jika password diisi
            hashed_password = generate_password_hash(password)
            cur.execute("""
                UPDATE user
                SET username = %s, email = %s, role = %s, password_hash = %s
                WHERE id = %s
            """, (username, email, role, hashed_password, id))
        else:  # Jika password kosong, hanya update data lain
            cur.execute("""
                UPDATE user
                SET username = %s, email = %s, role = %s
                WHERE id = %s
            """, (username, email, role, id))

        mysql.connection.commit()
        cur.close()

        flash('Pengguna berhasil diperbarui!', 'success')
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'Terjadi kesalahan: {e}', 'danger')
        return redirect(url_for('update_user', id=id))


@app.route('/delete_user/<int:id>', methods=['POST','GET'])
def delete_user(id):
    if 'id_user' not in session:
        return redirect(url_for('login'))

    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM user WHERE id = %s", [id])
        mysql.connection.commit()
        cur.close()
        flash('User deleted successfully!', 'success')
    except Exception as e:
        flash(f"Error: {e}", 'danger')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
