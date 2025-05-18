import time
from collections import defaultdict
from flask import Flask, request, abort, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'parol'


MAX_REQUESTS = 3
TIME_WINDOW = 60
MAX_LOGIN_ATTEMPTS = 5
BLOCK_TIME = 300


USERNAME = 'admin'
PASSWORD = 'parol'
LOG_FILE = 'log.txt'


request_counter = defaultdict(list)
login_attempts = defaultdict(int)
login_block_time = defaultdict(float)
blocked_ips = set()


WHITELIST_IPS = [
    '127.0.0.1',
    '192.168.1.126',
    # 'X.X.X.X'      
]


def log_ip(ip, status="OK"):
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    with open(LOG_FILE, 'a') as f:
        f.write(f"[{now}] IP: {ip} - {status}\n")


@app.before_request
def limit_remote_addr():
    ip = request.remote_addr
    now = time.time()


    if ip in WHITELIST_IPS:
        return


    if ip in blocked_ips:
        abort(403, description="Bu IP manzil bloklangan.")

    # IPdan kelayotgan so‘rovlar ro‘yxatini tozalash
    request_counter[ip] = [t for t in request_counter[ip] if now - t < TIME_WINDOW]
    request_counter[ip].append(now)

    if len(request_counter[ip]) > MAX_REQUESTS:
        blocked_ips.add(ip)
        log_ip(ip, status="BLOCKED - TOO MANY REQUESTS")
        abort(429, description="Too many requests - potential DDoS")
    else:
        log_ip(ip)


@app.route('/')
def index():
    return "Server ishlayapti. Xush kelibsiz!"



@app.route('/login', methods=['GET', 'POST'])
def login():
    ip = request.remote_addr
    now = time.time()


    if ip not in WHITELIST_IPS:

        if login_block_time[ip] > now:
            qolgan = int(login_block_time[ip] - now)
            return f" Ko‘p noto‘g‘ri urinishlar. {qolgan} soniyadan keyin urinib ko‘ring."

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            login_attempts[ip] = 0
            login_block_time[ip] = 0
            return redirect(url_for('admin_panel'))
        else:
            if ip not in WHITELIST_IPS:
                login_attempts[ip] += 1
                if login_attempts[ip] >= MAX_LOGIN_ATTEMPTS:
                    login_block_time[ip] = now + BLOCK_TIME
                    log_ip(ip, status="BLOCKED - TOO MANY LOGIN ATTEMPTS")
                    return f"Ko‘p noto‘g‘ri urinishlar. {BLOCK_TIME} soniyaga bloklandiz."
            return "Xato foydalanuvchi nomi yoki parol!", 401

    return render_template('login.html')



@app.route('/admin')
def admin_panel():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    try:
        with open(LOG_FILE, 'r') as f:
            logs = f.readlines()[-100:]
    except FileNotFoundError:
        logs = ["Log fayli topilmadi."]

    return render_template("admin.html", logs=logs, blocked_ips=blocked_ips)



@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
