# api/index.py
# This is a serverless wrapper. It attempts to load the Flask app and let Vercel
# run it as a function. Note: Flask as a long-running server may still fail on Vercel.
from importlib import import_module

# attempt to import your Flask app factory
try:
    # import your create_app and create an app object
    mod = import_module('app')
    app = mod.create_app()
except Exception as e:
    # If import fails, raise so logs show error
    raise

# Vercel serverless Python expects a function called `handler`.
# Here we try to use werkzeug's request/response to forward — simple approach:
from werkzeug.wrappers import Request, Response
from werkzeug.exceptions import HTTPException

@Request.application
def application(request):
    try:
        return app.full_dispatch_request()
    except HTTPException as ex:
        return ex
    except Exception as ex:
        raise

def handler(request):
    # Vercel's function runtime will call this handler (some runtimes call the module directly).
    return application(request)
