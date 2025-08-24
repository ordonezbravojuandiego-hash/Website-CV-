from flask import Flask, render_template, url_for, send_from_directory, abort
from data import inputs
import os

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.jinja_env.auto_reload = True

@app.context_processor
def inject_dict_for_all_templates():
    return dict(global_={"Last name": inputs["Last name"]})

@app.route("/")
def index():
    return render_template("index.html", data=inputs)

# Sanidad: ruta simple para comprobar que el servidor responde
@app.route("/__ping")
def __ping():
    return "OK - " + inputs.get("First name", "??")

# Descargar CV
@app.route("/download/cv")
def download_cv():
    filename = "Juan_Diego_Ordonez_CV.pdf"   # nombre ASCII que estás usando
    cv_dir = os.path.join(app.root_path, "static", "cv")
    path = os.path.join(cv_dir, filename)
    if not os.path.isfile(path):
        abort(404)
    return send_from_directory(cv_dir, filename, as_attachment=True, mimetype="application/pdf")

if __name__ == "__main__":
    # host y puerto explícitos para no confundirse
    app.run(host="127.0.0.1", port=5000, debug=True)




