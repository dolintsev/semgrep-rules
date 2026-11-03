import os
import shlex
import subprocess

from flask import Flask, request

app = Flask(__name__)


@app.route("/popen", methods=["POST"])
def popen():
    domain = request.form.get("domain", "")
    command = f"dig {domain}"
    # ruleid: flask-command-injection-shell
    return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).communicate()[0]


@app.route("/system")
def system():
    host = request.args.get("host", "")
    # ruleid: flask-command-injection-shell
    os.system("ping -c 1 " + host)
    return "ok"


@app.route("/quoted")
def quoted():
    host = shlex.quote(request.args.get("host", ""))
    # ok: flask-command-injection-shell
    os.system("ping -c 1 " + host)
    return "ok"


@app.route("/list")
def as_list():
    domain = request.args.get("domain", "")
    # ok: flask-command-injection-shell
    return subprocess.run(["dig", domain], capture_output=True).stdout


def constant():
    # ok: flask-command-injection-shell
    return subprocess.run("uptime", shell=True, capture_output=True).stdout

@app.route("/os-popen")
def os_popen():
    host = request.args.get("host", "")
    # ruleid: flask-command-injection-shell
    return os.popen("ping -c 1 " + host).read()
