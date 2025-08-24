# 










from flask import Flask, render_template, request, redirect, url_for, session, flash
import bankcore, accounts
import inspect

app = Flask(__name__)
app.secret_key = "change-this-key"

def _create_account_bridge(name, password, user_number_opt=None):
    """Bridge function to support both possible create_account signatures."""
    try:
        params = inspect.signature(bankcore.create_account).parameters
        param_count = len(params)
    except Exception:
        param_count = 2

    if param_count >= 3:  # create_account(name, id, password)
        branch = getattr(bankcore, "branch_id", "0000")
        if not user_number_opt or not user_number_opt.strip():
            raise ValueError("User number is required to form the customer ID.")
        customer_id = f"{branch}-{user_number_opt.strip()}"
        bankcore.create_account(name, customer_id, password)
        return customer_id
    else:  # create_account(name, password)
        return bankcore.create_account(name, password)


@app.route("/")
def home():
    return render_template("index.html")


# @app.route("/create_account", methods=["GET", "POST"])
# def create_account_route():
#     if request.method == "POST":
#         name = request.form["name"].strip()
#         password = request.form["password"]
#         user_number = request.form.get("user_number", "").strip()

#         try:
#             customer_id = _create_account_bridge(name, password, user_number)
#             accounts.deposit(customer_id, 0)  # initialize balance
#             session["user"] = customer_id
#             flash(f"Account created successfully! 🎉 Your ID: {customer_id}", "success")
#             return redirect(url_for("dashboard"))
#         except Exception as e:
#             flash(str(e), "error")

#     needs_user_number = len(inspect.signature(bankcore.create_account).parameters) >= 3
#     return render_template("create_account.html",
#                            needs_user_number=needs_user_number,
#                            branch_id=getattr(bankcore, "branch_id", "0000"))


# @app.route("/create_account", methods=["GET", "POST"])
# def create_account_route():
#     if request.method == "POST":
#         name = request.form["name"].strip()
#         password = request.form["password"]

#         # directly call your existing bankcore function
#         customer_id = bankcore.create_account(name, password)

#         # initialize balance
#         accounts.deposit(customer_id, 0)

#         # log user in immediately
#         session["user"] = customer_id

#         flash(f"Account created successfully! 🎉 Your ID: {customer_id}", "success")
#         return redirect(url_for("dashboard"))

#     return render_template("create_account.html")



# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         customer_id = request.form["customer_id"].strip()
#         password = request.form["password"]
#         if bankcore.login(customer_id, password):
#             session["user"] = customer_id
#             flash("Login successful ✅", "success")
#             return redirect(url_for("dashboard"))
#         flash("Invalid login ❌", "error")
#     return render_template("login.html")


# @app.route("/dashboard")
# def dashboard():
#     if "user" not in session:
#         return redirect(url_for("login"))
#     cid = session["user"]
#     balance = accounts.check_balance(cid)
#     return render_template("dashboard.html", customer_id=cid, balance=balance)


# @app.route("/deposit", methods=["POST"])
# def deposit():
#     if "user" not in session:
#         return redirect(url_for("login"))
#     try:
#         amount = float(request.form["amount"])
#         accounts.deposit(session["user"], amount)
#         flash(f"Deposited {amount} ✅", "success")
#     except Exception:
#         flash("Invalid deposit ❌", "error")
#     return redirect(url_for("dashboard"))


# @app.route("/withdraw", methods=["POST"])
# def withdraw():
#     if "user" not in session:
#         return redirect(url_for("login"))
#     try:
#         amount = float(request.form["amount"])
#         accounts.withdraw(session["user"], amount)
#         flash(f"Withdrew {amount} ✅", "success")
#     except Exception:
#         flash("Invalid withdrawal ❌", "error")
#     return redirect(url_for("dashboard"))


# @app.route("/logout")
# def logout():
#     session.pop("user", None)
#     flash("Logged out successfully 👋", "info")
#     return redirect(url_for("home"))


# if __name__ == "__main__":
#     app.run(debug=True)





















from flask import Flask, render_template, request, redirect, url_for, session, flash
from banking_app_py import bankcore, accounts
import inspect

app = Flask(__name__)
app.secret_key = "change-this-key"  # must be set for session + flash to work


# ---------- Helper Functions ----------

def _extract_last_key_from_dict(d):
    try:
        return next(reversed(d))
    except Exception:
        keys = list(d.keys())
        return keys[-1] if keys else None

def _find_customer_id_by_name(d, name):
    for k, v in reversed(list(d.items())):
        if isinstance(v, dict):
            if v.get("name") == name or v.get("Name") == name:
                return k
        if isinstance(v, (list, tuple)) and len(v) > 0:
            if v[0] == name:
                return k
    return None

def _get_customer_id_after_create(retval, name=None):
    """Figure out the new customer_id if create_account did not return it."""
    if retval and isinstance(retval, str) and retval.strip():
        return retval.strip()

    branch = getattr(bankcore, "branch_id", None)

    # check common dicts
    for dict_name in ["_users_info", "Users_Info", "users_info", "users"]:
        if hasattr(bankcore, dict_name):
            d = getattr(bankcore, dict_name)
            if isinstance(d, dict) and d:
                found = _find_customer_id_by_name(d, name)
                if found:
                    return found
                last = _extract_last_key_from_dict(d)
                if last:
                    return str(last)

    # look for any dict key starting with branch-id
    if branch:
        for attr in dir(bankcore):
            try:
                val = getattr(bankcore, attr)
            except Exception:
                continue
            if isinstance(val, dict) and val:
                for k in reversed(list(val.keys())):
                    if isinstance(k, str) and k.startswith(str(branch) + "-"):
                        return k

    # fallback: use user_counter
    for c in ["_user_counter", "user_counter"]:
        if hasattr(bankcore, c):
            try:
                cnt = int(getattr(bankcore, c))
                if branch:
                    return f"{branch}-{cnt}"
            except Exception:
                pass

    return None


# ---------- Routes ----------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/create_account", methods=["GET", "POST"])
def create_account_route():
    if request.method == "POST":
        name = request.form["name"].strip()
        password = request.form["password"]

        try:
            retval = bankcore.create_account(name, password)
        except TypeError:
            # in case their function has different signature
            try:
                sig = inspect.signature(bankcore.create_account)
                if len(sig.parameters) >= 3:
                    branch = getattr(bankcore, "branch_id", "0000")
                    guessed_id = None
                    if hasattr(bankcore, "_user_counter"):
                        guessed_id = f"{branch}-{getattr(bankcore, '_user_counter')}"
                    retval = bankcore.create_account(name, guessed_id or "", password)
                else:
                    retval = bankcore.create_account(name, password)
            except Exception as e:
                flash("Failed to create account: " + str(e), "error")
                return render_template("create_account.html")

        # deduce customer_id
        customer_id = _get_customer_id_after_create(retval, name)

        if customer_id:
            try:
                accounts.deposit(customer_id, 0)  # initialize balance
            except Exception:
                pass
            session["user"] = customer_id
            flash(f"Account created successfully! 🎉 Your ID: {customer_id}", "success")
            return redirect(url_for("dashboard"))

        flash("Account created but could not determine your Customer ID. "
              "Please check the server console.", "error")
        return redirect(url_for("login"))

    return render_template("create_account.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        customer_id = request.form["customer_id"].strip()
        password = request.form["password"]
        if bankcore.login(customer_id, password):
            session["user"] = customer_id
            flash("Login successful ✅", "success")
            return redirect(url_for("dashboard"))
        flash("Invalid login ❌", "error")
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    cid = session["user"]
    balance = accounts.check_balance(cid)
    return render_template("dashboard.html", customer_id=cid, balance=balance)


@app.route("/deposit", methods=["POST"])
def deposit():
    if "user" not in session:
        return redirect(url_for("login"))
    try:
        amount = float(request.form["amount"])
        accounts.deposit(session["user"], amount)
        flash(f"Deposited {amount} ✅", "success")
    except Exception:
        flash("Invalid deposit ❌", "error")
    return redirect(url_for("dashboard"))


@app.route("/withdraw", methods=["POST"])
def withdraw():
    if "user" not in session:
        return redirect(url_for("login"))
    try:
        amount = float(request.form["amount"])
        accounts.withdraw(session["user"], amount)
        flash(f"Withdrew {amount} ✅", "success")
    except Exception:
        flash("Invalid withdrawal ❌", "error")
    return redirect(url_for("dashboard"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out successfully 👋", "info")
    return redirect(url_for("home"))


# ---------- Run ----------
if __name__ == "__main__":
    app.run(debug=True)
