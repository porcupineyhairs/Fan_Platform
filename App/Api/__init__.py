from flask import blueprints


v1 = blueprints.Blueprint("V1", __name__, url_prefix="/api")

from . import index,userOpt,errors_and_auth,projectOpt


