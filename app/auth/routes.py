from flask import Blueprint, jsonify, request
from app.auth import functionality as func
from datetime import timedelta

bp_auth = Blueprint('bp_auth', __name__, url_prefix='/auth')
