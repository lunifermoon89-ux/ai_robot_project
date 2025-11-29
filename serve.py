from app import app
import os

def run():
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', '8080'))
    try:
        # Prefer waitress in production on Windows
        from waitress import serve
        print('Starting server with waitress on %s:%s' % (host, port))
        serve(app, host=host, port=port)
    except Exception:
        print('Waitress not available; falling back to Flask development server')
        app.run(host=host, port=port)


if __name__ == '__main__':
    run()
