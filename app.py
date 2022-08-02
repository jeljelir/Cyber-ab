from flask import Flask, render_template, request, url_for, redirect, session
import subprocess
import time, os, uuid
from datetime import datetime, timedelta
from ast import literal_eval
from flask_session import Session


app = Flask(__name__)
app.config['SECRET_KEY'] = uuid.uuid4().hex
app.config["SESSION_PERMANENT"] = timedelta(minutes=5)
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

total_scan = 1


# sanitize strings; probably there is no need as Flask is smart enough
def sanitizer(string):
    string = str(string)
    string = string.replace("[", "")
    string = string.replace("]", "")
    string = string.replace("{", "")
    string = string.replace("}", "")
    string = string.replace("<", "")
    string = string.replace("?", "")
    string = string.replace(" ", "")
    string = string.replace(":", "")
    string = string.replace(";", "")
    string = string.replace("-", "")
    string = string.replace("_", "")
    string = string.replace(".", "")
    string = string.replace("\\", "")
    string = string.replace("/", "")
    return string


# check answers and act accordingly
def question(ans, c_ans):
    answer = sanitizer(ans).lower()
    if answer in c_ans:
        flag = 0
    else:
        flag = 2
    print("\n\n\t Flag: ", flag, "\n\n", ans)
    return flag


# id generator
def id_gen():
    if "counter" in session:
        session["counter"] += 1
    else:
        session["counter"] = 1
    print("\n\n\n\n\t Counter: ", session["counter"], "\n\n\n\n")
    
    global total_scan
    if total_scan < session["counter"]:
        total_scan += session["counter"]
    return session["counter"]


# add to sessions
def add_msg_session(message):
    if "msg" in session:
        session["msg"].append(message)
    else:
        session["msg"] = [message]

# app class
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tools/')
def tools():
    global total_scan
    if "msg" in session and session["msg"]:
        sorted_messages = sorted(session["msg"], key=lambda d: d['id'], reverse=True)
    else:
        sorted_messages = None
    return render_template('tools.html', messages=sorted_messages, scans=total_scan)

@app.route('/nmap/', methods=('GET', 'POST'))
def nmap():
    global total_scan
    
    if request.method == 'POST':
        print(request.form['command'])
        print(request.form['passphrase'])
        
        if request.form['passphrase'] != 'Fr!3nds':
           add_msg_session({'title': 'Nmap Scan on', 'host': request.form['host'], 'content': 'Wrong passphrase', 'id': id_gen(), 'time': datetime.now().strftime("%d/%m/%Y %H:%M:%S")})
           return redirect(url_for('tools'))

        command = request.form['command']
        command = command.split()

        cmd2 = subprocess.Popen(['sudo', '-S'] + command, stdout=subprocess.PIPE)

        output = cmd2.stdout.read().decode()
        
        print(output)
        
        # write the result on the home page
        add_msg_session({'title': 'Nmap Scan on', 'host': request.form['host'], 'content': output, 'id': id_gen(), 'time': datetime.now().strftime("%d/%m/%Y %H:%M:%S")})
        total_scan += 1
        return redirect(url_for('tools'))
    return render_template('nmap.html')

@app.route('/wapiti/', methods=('GET', 'POST'))
def wapiti():
    global total_scan
    if request.method == 'POST':
        print(request.form['command'])
        print(request.form['passphrase'])
        
        if request.form['passphrase'] != 'Fr!3nds':
           add_msg_session({'title': 'Wapiti Vulnerability Scan on', 'host': request.form['host'], 'content': 'Wrong passphrase', 'id': id_gen(), 'time': datetime.now().strftime("%d/%m/%Y %H:%M:%S")})
           return redirect(url_for('tools'))

        report_path = '/home/ali/milad/results/result.txt'
        command = request.form['command'] + ' -f txt -o {0}'.format(report_path)
        command = command.split()

        cmd = subprocess.Popen(command, stdout=subprocess.PIPE)

        output = cmd.stdout.read().decode()
        # sanitize the output as it will be shown to the public
        output = output.replace('/home/ali/milad', '')
        output = output.split('A report has been generated', 1)[0] + '\n'
        time.sleep(2)
        output += open(report_path).read()

        print(output)

        # remove the generated report to not mixed up with the new one
        if os.path.exists(report_path):
            os.remove(report_path)
            print('The report file was deleted')
        else:
            print('The report file does not exist')

        # write the result on the home page
        add_msg_session({'title': 'Wapiti Vulnerability Scan on', 'host': request.form['host'], 'content': output, 'id': id_gen(), 'time': datetime.now().strftime("%d/%m/%Y %H:%M:%S")})
        total_scan += 1
        return redirect(url_for('tools'))

    return render_template('wapiti.html')

@app.route('/sslyze/', methods=('GET', 'POST'))
def sslyze():
    global total_scan
    if request.method == 'POST':
        print(request.form['command'])
        print(request.form['passphrase'])
        
        if request.form['passphrase'] != 'Fr!3nds':
           add_msg_session({'title': 'SSLyze Certificate Scan on', 'host': request.form['host'], 'content': 'Wrong passphrase', 'id': id_gen(), 'time': datetime.now().strftime("%d/%m/%Y %H:%M:%S")})
           return redirect(url_for('tools'))

        command = 'python3 -m ' + request.form['command']
        command = command.split()

        cmd = subprocess.Popen(command, stdout=subprocess.PIPE)

        output = cmd.stdout.read().decode()

        print(output)

        # write the result on the home page
        add_msg_session({'title': 'SSLyze Certificate Scan on ', 'host': request.form['host'], 'content': output, 'id': id_gen(), 'time': datetime.now().strftime("%d/%m/%Y %H:%M:%S")})
        total_scan += 1
        return redirect(url_for('tools'))
    return render_template('sslyze.html')

@app.route('/about/', methods=('GET', 'POST'))
def about():
     return render_template('about.html')

@app.route('/course01/')
def course01():
    return render_template('course01.html')

@app.route('/course02/', methods=('GET', 'POST'))
def course02():
    flag = 1
    response = 'EMPTY'
    correct_answer = ["easyflag"]
    if request.method == 'POST':
        response = request.form['question']
        flag = question(response, correct_answer)
    return render_template('course02.html', flag=flag, answer=response)

@app.route('/course03/', methods=('GET', 'POST'))
def course03():
    flag = 1
    response = 'EMPTY'
    correct_answer = ["ca1cu1at1ngmach1n3s1bb4c", "picoctfca1cu1at1ngmach1n3s1bb4c"]
    if request.method == 'POST':
        response = request.form['question']
        flag = question(response, correct_answer)
    return render_template('course03.html', flag=flag, answer=response)

@app.route('/course04/', methods=('GET', 'POST'))
def course04():
    flag = 1
    response = 'EMPTY'
    correct_answer = ["phishing"]
    if request.method == 'POST':
        response = request.form['question']
        flag = question(response, correct_answer)
    return render_template('course04.html', flag=flag, answer=response)

@app.route('/course05/', methods=('GET', 'POST'))
def course05():
    flag = 1
    response = 'EMPTY'
    correct_answer = ["centos", "ubuntu"]
    if request.method == 'POST':
        response = request.form['question']
        flag = question(response, correct_answer)
    return render_template('course05.html', flag=flag, answer=response)

@app.route('/course06/', methods=('GET', 'POST'))
def course06():
    flag = 1
    response = 'EMPTY'
    correct_answer = ["zeroday", "0day"]
    if request.method == 'POST':
        response = request.form['question']
        flag = question(response, correct_answer)
    return render_template('course06.html', flag=flag, answer=response)

@app.route('/course07/', methods=('GET', 'POST'))
def course07():
    flag = 1
    response = 'EMPTY'
    correct_answer = ["iamtheflag"]
    if request.method == 'POST':
        response = request.form['question']
        flag = question(response, correct_answer)
    return render_template('course07.html', flag=flag, answer=response)

@app.route('/course08/', methods=('GET', 'POST'))
def course08():
    flag = 1
    response = 'EMPTY'
    correct_answer = ["453332156"]
    if request.method == 'POST':
        response = request.form['question']
        flag = question(response, correct_answer)
    return render_template('course08.html', flag=flag, answer=response)

@app.route('/course09/', methods=('GET', 'POST'))
def course09():
    flag = 1
    response = 'EMPTY'
    correct_answer = ["yes"]
    if request.method == 'POST':
        response = request.form['question']
        flag = question(response, correct_answer)
    return render_template('course09.html', flag=flag, answer=response)

@app.route('/course10/', methods=('GET', 'POST'))
def course10():
    flag = 1
    response = 'EMPTY'
    correct_answer = ["yes", "w3cnowthatwehavetherightbrowserletsgetthepartystarted", "nowthatwehavetherightbrowserletsgetthepartystarted"]
    if request.method == 'POST':
        response = request.form['question']
        flag = question(response, correct_answer)
    return render_template('course10.html', flag=flag, answer=response)

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000)
