import os
from decouple import config

from api import create_app
from api.config.config import config_dict


app = create_app(config=config_dict[config("ENV", "dev")])

if __name__ == "__main__":
    app.run()
