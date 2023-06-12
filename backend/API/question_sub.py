import os
import sys
from flask import jsonify,Blueprint,request

sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
import database as DB

api_module = Blueprint("sub",__name__,url_prefix="/sub")