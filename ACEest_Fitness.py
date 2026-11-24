"""Assignment-named Flask entry point for ACEest Fitness and Gym.

The application factory and implementation remain in ``app.py``/``aceest``;
this file provides the filename requested by the assignment and is also a
direct WSGI entry point for local execution.
"""

from app import app


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
