import os

# from app import app
from EagleBotWebUI.app import app

port = int(os.getenv('PORT', 4000))

print("Starting app on port %d" % port)

app.run(debug=True, port=port, host='0.0.0.0')