import jwt
import datetime
import flask

JWT_KEY = "JyhYhuuJhh8998t8889HJGUYkubitTR7b87875l8977987"



def jwtGenerate(user_id: str, user_name: str, minutes=15):
    now = datetime.datetime.now(datetime.UTC)
    payload = {
        "sub": str(user_id),
        "user_name": str(user_name),
        "iat": now,
        "exp": now + datetime.timedelta(minutes=minutes)
    }
    return jwt.encode(payload, JWT_KEY, algorithm='HS256')



def jwtDecode(jwt_token:str):
    return jwt.decode(jwt_token, key=JWT_KEY, algorithms=['HS256', ])


def jwtCheckAndRegenerate(decoded_jwt: dict):
    exp = datetime.datetime.fromtimestamp(decoded_jwt["exp"], datetime.UTC)
    now = datetime.datetime.now(datetime.UTC)

    remaining = (exp - now).total_seconds()

    # Sliding window: refresh if less than 2 minutes left
    if remaining < 120: 
        return jwtGenerate(decoded_jwt["sub"], decoded_jwt["user_name"])
    
    return None

    
#auth check decorator
def authCheck(func):
    def wrapper(*args, **kwargs):
        auth_header = flask.request.headers.get("Authorization")

        if not auth_header:
            return {"error": "Missing Authorization header"}, 401
        
        # Support Bearer <token>
        if auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
        else:
            token = auth_header

        try:
            print(type(token))
            decoded = jwtDecode(str(token))

        except Exception as e:
            print(e)
            return {"error": "Invalid or expired token"}, 401

        # Attach user to request context
        flask.g.user_id = decoded["sub"]
        flask.g.user_name = decoded["user_name"]

        # Check if token needs sliding refresh
        refreshed = jwtCheckAndRegenerate(decoded)
        # print(refreshed)

        result = func(*args, **kwargs)

        # If regenerate, attach refreshed token
        if refreshed:
            if isinstance(result, tuple):
                body, code = result
                response = flask.make_response(body, code)
            else:
                response = flask.make_response(result)

            response.headers["Authorization"] = f"{refreshed}"
            return response
        
        return result

    wrapper.__name__ = func.__name__
    return wrapper

    



if __name__ == '__main__':
    a = jwtGenerate("12","halo",minutes=1)
    b = jwtDecode(a)
    print(a)
    print(b)