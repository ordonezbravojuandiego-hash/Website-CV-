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

# --- Visualización de CV (ES/EN) ---
CV_FILES = {
    "es": os.getenv("CV_FILENAME_ES", "Juan_Diego_Ordonez_CV.pdf"),
    "en": os.getenv("CV_FILENAME_EN", "Juan_Diego_Ordonez_CV_EN.pdf"),
}

def _cv_dir():
    return os.path.join(app.root_path, "static", "cv")

def _file_exists(filename: str) -> bool:
    return os.path.isfile(os.path.join(_cv_dir(), filename))

@app.route("/download/cv/<lang>")
def download_cv_lang(lang):
    lang = (lang or "").lower()
    filename = CV_FILES.get(lang)
    if not filename or not _file_exists(filename):
        abort(404)
    # CORRECCIÓN: as_attachment=False permite que el navegador lo abra en lugar de descargarlo
    return send_from_directory(_cv_dir(), filename, as_attachment=False, mimetype="application/pdf")

# compat: /download/cv -> español
@app.route("/download/cv")
def download_cv():
    filename = CV_FILES["es"]
    if not _file_exists(filename):
        abort(404)
    # CORRECCIÓN: as_attachment=False para visualización directa
    return send_from_directory(_cv_dir(), filename, as_attachment=False, mimetype="application/pdf")





