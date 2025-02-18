import logging

from flask_smorest import Blueprint

warm_up_controller = Blueprint("WarmUpController", __name__, description="Warm Up API")

@warm_up_controller.route("/warmup")
@warm_up_controller.response(200)
def get_warmup():
    return "Warm Up endpoint executed."