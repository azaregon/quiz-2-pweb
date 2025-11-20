import flask
import app.dbmodel as dbmodel
from app.helper import authHelper as auth
import datetime

project_bp = flask.Blueprint('project_bp',__name__,url_prefix="/project")

def serialize_project(project: dbmodel.PROJECTS):
    """Helper function to convert a project ORM object to a dictionary."""
    if not project:
        return None
    
    collaborators = [
        {
            "user_id": collab.USER_.ID,
            "user_name": collab.USER_.user_name,
            "role": collab.role
        } for collab in project.COLLABORATORS
    ]

    tech_stack = [
        {
            "tech_id": tech.PROJECT_TECHS.ID,
            "tech_name": tech.PROJECT_TECHS.tech_name,
            "tech_color": tech.PROJECT_TECHS.tech_color
        } for tech in project.PROJECT_TECH_STACK
    ]

    return {
        "id": project.ID,
        "project_manager_id": project.USER_ID_PM,
        "status_id": project.PROJECT_STATUS_ID,
        "project_name": project.project_name,
        "project_desc": project.project_desc,
        "project_start": project.project_start.isoformat() if isinstance(project.project_start, datetime.date) else None,
        "project_date": project.project_date.isoformat() if isinstance(project.project_date, datetime.date) else None,
        "project_links": project.project_links,
        "collaborators": collaborators,
        "technologies": tech_stack
    }

@project_bp.route("/statuses", methods=['GET'])
def get_statuses():
    """Endpoint to get all available project statuses."""
    statuses = dbmodel.getAllProjectStatuses()
    return flask.jsonify({"success": True, "data": statuses}), 200

@project_bp.route("/technologies", methods=['GET'])
def get_techs():
    """Endpoint to get all available project statuses."""
    statuses = dbmodel.getAllProjectTechs()
    return flask.jsonify({"success": True, "data": statuses}), 200


@project_bp.route("/new", methods=['POST'])
@auth.authCheck
def newProject():
    json_data = flask.request.get_json()
    if not json_data:
        return flask.jsonify({"success": False, "error_message": "Request must be JSON"}), 400

    # Set the project manager to the logged-in user for security
    json_data['USER_ID_PM'] = flask.g.user_id

    try:
        result = dbmodel.createNewProject(json_data)
        return flask.jsonify(result), 201
    except Exception as e:
        return flask.jsonify({"success": False, "error_message": str(e)}), 500

@project_bp.route("/<int:project_id>", methods=['GET'])
@auth.authCheck
def get_project(project_id):
    project = dbmodel.getProjectRaw(project_id)
    if not project:
        return flask.jsonify({"success": False, "error_message": "Project not found"}), 404
    
    # The getProjectRaw function returns a dictionary-like object, so we can directly jsonify it.
    return flask.jsonify({"success": True, "data": dict(project)}), 200


@project_bp.route("/all/<user_id>", methods=['GET'])
def geAllProject(user_id):
    all_project = dbmodel.getAllProject(user_id)
    if not all_project:
        return flask.jsonify({"success": False, "error_message": "Project not found"}), 200
    
    # The getProjectRaw function returns a dictionary-like object, so we can directly jsonify it.
    return flask.jsonify({"success": True, "data": all_project}), 200

@project_bp.route("/delete/<int:project_id>", methods=['DELETE'])
@auth.authCheck
def deleteProject(project_id):
    """Endpoint to delete a project. Only the project manager can delete it."""
    user_id = flask.g.user_id  # Get the logged-in user's ID from the auth decorator
    try:
        result = dbmodel.deleteProject(project_id, user_id)
        if not result.get("success"):
            return flask.jsonify(result), 403 # Forbidden or Not Found
        return flask.jsonify(result), 200
    except Exception as e:
        return flask.jsonify({"success": False, "error_message": str(e)}), 500
