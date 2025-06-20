from flask import Blueprint, render_template, redirect, request, url_for
from .config import basic_auth
from .admin import handle_admin_action

admin_bp = Blueprint('admin_routes', __name__)

@admin_bp.route('/admin_dashboard')
@basic_auth.required
def admin_dashboard():
    return render_template('admin/index.html')

@admin_bp.route('/admin_dashboard/control', methods=['POST'])
@basic_auth.required
def admin_control():
    action = request.form.get('action')
    handle_admin_action(action)
    return redirect(url_for('admin_routes.admin_dashboard'))
