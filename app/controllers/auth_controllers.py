import flask
import app.dbmodel as dbmodel
from app.helper import authHelper as auth

#prefix /api/auth/logout
auth_bp = flask.Blueprint('auth_bp',__name__,url_prefix="/auth")



@auth_bp.route("/login", methods=['POST'])
def login():
    # user_name = flask.request.form.get("user_name")
    # password = flask.request.form.get("password")
    json_data = flask.request.json
    user_name = json_data.get("user_name")
    password = json_data.get("password")


    check_condition = (user_name and 
                       password)

    if not check_condition:
        return flask.jsonify(
            {
                "success": False,
                "error_message": "Given credential is empty"
            }
        )
    
    # authentication

    getted_user = dbmodel.getUserDetails(user_name)
    if not getted_user:
        resp = flask.make_response(flask.jsonify(
                        {
                            "success": False,
                            "error_message": "username or password is not correct"
                        }, 401
                    )
                )
        return resp

    pw_check = getted_user.checkPassword(password)

    if pw_check == True: #if password is correct
        token = auth.jwtGenerate(getted_user.ID, getted_user.user_name)
        return flask.jsonify({
                "success" : True,
                "message": "Login successful",
                "token": token
            }), 200
    else:
        resp = flask.make_response(flask.jsonify(
                        {
                            "success": False,
                            "error_message": "username or password is not correct"
                        }, 401
                    )
                )
        return resp

@auth_bp.route('/logout')
def logout():
    # flask.session.pop("ID",default=None)
    # flask.session.pop("user_name",default=None)

    return flask.jsonify({
        "success" : True,
        "url_redirect" : "/"
    })
    
@auth_bp.route('/register', methods=['POST'])
def register():
    # user_name = flask.request.form.get("user_name")
    # password = flask.request.form.get("password")
    json_data = flask.request.json
    user_name = json_data.get("user_name")
    password = json_data.get("password")

    check_condition = (user_name and 
                       password)

    if not check_condition:
        return flask.jsonify(
            {
                "success": False,
                "error_message": "Given credential is empty"
            }
        )
    


    # register
    getted_user = dbmodel.getUserDetails(user_name)

    if getted_user:
        return flask.jsonify({
            "success": False,
            "error_message": "user name already taken"
        })
    

    create_user = dbmodel.createNewUser(
        user_name=user_name,
        passwd=password
    )

    getted_user_2 = dbmodel.getUserDetails(user_name)

    token = auth.jwtGenerate(getted_user_2.ID, getted_user_2.user_name)
    return flask.jsonify({
            "success" : True,
            "message": "Login successful",
            "token": token
        }), 200
    
    




    

    
