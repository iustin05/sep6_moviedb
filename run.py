import os

from app import create_app

app = create_app()

if __name__ == '__main__':
    environment_config = os.environ.get("DEPLOYMENT_ENV", "development")
    if environment_config == "development":
        port = 5000
        debug_mode = True
    elif environment_config == "production":
        port = 80
        debug_mode = False
    else:
        raise ValueError("Invalid deployment environment specified and server tried to start.")
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
