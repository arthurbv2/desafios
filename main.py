from app import app
from crawlers.views import views
import strings

app.run(port=8181, host='0.0.0.0', threaded=True, ssl_context='adhoc')