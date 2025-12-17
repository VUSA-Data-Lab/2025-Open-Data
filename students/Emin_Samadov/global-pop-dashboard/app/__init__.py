from flask import Flask
from .data_loader import load_clean_data
from .processor import get_country_list
import os


def create_app(clean_data_path: str) -> Flask:
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    app = Flask(
        __name__,
        template_folder=os.path.join(base_dir, "templates"),
        static_folder=os.path.join(base_dir, "static")
    )

    df = load_clean_data(clean_data_path)
    app.config["POPULATION_DF"] = df
    app.config["COUNTRIES"] = get_country_list(df)

    from .webapp import webapp
    app.register_blueprint(webapp)


    return app
