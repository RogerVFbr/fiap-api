import logging

from flask_smorest import Blueprint

warm_up_controller = Blueprint("WarmUpController", __name__, description="Warm Up API")

LOGGER = logging.getLogger(__name__)

@warm_up_controller.route("/warmup")
@warm_up_controller.response(200)
def get_warmup():
    LOGGER.info("Warm Up endpoint called.")
    return "Warm Up endpoint executed."