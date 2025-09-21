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

# --- Descarga de CV (ES/EN) con nombres configurables por entorno ---
CV_FILES = {
    # Puedes cambiar esto en Heroku con:
    # heroku config:set CV_FILENAME_ES=TuNombre.pdf
    # heroku config:set CV_FILENAME_EN=TuNombre_EN.pdf
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
    if not filename:
        abort(404)  # idioma no soportado
    if not _file_exists(filename):
        abort(404)  # archivo no encontrado en static/cv
    return send_from_directory(_cv_dir(), filename, as_attachment=True, mimetype="application/pdf")

# Ruta antigua (compat): /download/cv -> CV en español
@app.route("/download/cv")
def download_cv():
    filename = CV_FILES["es"]
    if not _file_exists(filename):
        abort(404)
    return send_from_directory(_cv_dir(), filename, as_attachment=True, mimetype="application/pdf")





