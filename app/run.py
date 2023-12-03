import os

from starting import create_app

port = int(os.environ.get("PORT", 5000))
debug_mode = True if port == 5000 else False

if __name__ == '__main__':
    app = create_app()
    print('test')
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
