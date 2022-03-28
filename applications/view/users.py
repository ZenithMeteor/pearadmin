from flask import render_template
from flask_login import login_required, current_user
from sqlalchemy import desc

from common.utils.rights import permission_required, view_logging_required
from models import LogModel, RoleModel, UserModel
from . import index_bp


# 用户增加
@index_bp.get('/users/')
@view_logging_required
@permission_required("admin:user:main")
def users_main():
    return render_template('admin/users/users.html')


@index_bp.get('/users/add')
@view_logging_required
@permission_required("admin:user:add")
def users_add_view():
    roles = RoleModel.query.all()
    return render_template('admin/users/users_add.html', roles=roles)


@index_bp.get('/users/<user_id>')
@view_logging_required
@permission_required("admin:user:edit")
def users_user_id_view(user_id):
    #  获取编辑用户信息
    user = UserModel.query.filter_by(id=user_id).first()
    roles = RoleModel.query.all()
    checked_roles = []
    for r in user.role:
        checked_roles.append(r.id)
    return render_template('admin/users/users_edit.html', user=user, roles=roles, checked_roles=checked_roles)


@index_bp.get('/users/center')
@login_required
def users_center():
    user_logs = LogModel.query.filter_by(url='/passport/login').filter_by(uid=current_user.id).order_by(
        desc(LogModel.create_at)).limit(10)
    return render_template('admin/users/profile.html', user_info=current_user, user_logs=user_logs)


@index_bp.get('/users/avatar')
def users_avatar_view():
    return render_template('admin/users/profile_avatar.html')
