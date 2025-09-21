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

# Descargar CV por idioma (ES/EN)
@app.route("/download/cv/<lang>")
def download_cv_lang(lang):
    # Mapear idioma a archivo (nombre ASCII para evitar problemas)
    cv_map = {
        "es": "Juan_Diego_Ordonez_CV.pdf",       # ya existente
        "en": "Juan_Diego_Ordonez_CV_EN.pdf",    # súbelo a static/cv/
    }
    filename = cv_map.get(lang.lower())
    if not filename:
        abort(404)

    cv_dir = os.path.join(app.root_path, "static", "cv")
    path = os.path.join(cv_dir, filename)
    if not os.path.isfile(path):
        abort(404)

    return send_from_directory(cv_dir, filename, as_attachment=True, mimetype="application/pdf")





