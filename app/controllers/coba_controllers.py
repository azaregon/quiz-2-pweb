import flask
import app.dbmodel
from app.helper.authHelper import * 


coba_bp = flask.Blueprint('coba_bp',__name__,url_prefix="/coba")

@coba_bp.route("/ll",methods=['GET'])
@authCheck
def coba():
    return f"hello id {flask.g.get("user_id")} with name {flask.g.get("user_name")}"