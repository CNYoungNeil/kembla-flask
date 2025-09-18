from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

from app.common.result import Result
from app.services import user_service
from app.services.user_service import authenticate, get_user_list

bp = Blueprint("user", __name__)

# 用户登录
@bp.route("/login", methods=["POST"])
def login():
	data = request.get_json()
	account = data.get("account")
	password = data.get("password")

	user = authenticate(account, password)  #service方法进行验证密码
	if not user:
		return Result.fail("账号或密码错误")

	token = create_access_token(
		identity=str(user.user_id),
		expires_delta=timedelta(days=1)
	)

	return Result.success({
		"token": token,
		"user": user.to_dict()
	})

# 条件分页查询
@bp.route("/listPage", methods=["POST"])
def list_page():
	params = request.get_json()

	name = params.get("name", "")
	account = params.get("account", "")
	identity_id = params.get("identityId", "")
	page_num = params.get("pageBody", {}).get("pageNum", 1)
	page_size = params.get("pageBody", {}).get("pageSize", 10)

	# 调用 service
	data = get_user_list(name, account, identity_id, page_num, page_size)
	return Result.success(data)


# 新增用户create
@bp.route("/save", methods=["POST"])
def save_user():
	try:
		data = request.get_json()

		# 调用 service 层方法
		new_user = user_service.create_user(data)

		return Result.success(new_user.to_dict())
	except Exception as e:
		# 打印日志可选
		print(f"Error creating user: {e}")
		return Result.fail("Failed to create user")

# 删除订单
@bp.route("/delete", methods=["DELETE"])
def delete_user_api():
	user_id = request.args.get("id")
	if not user_id:
		return Result.error("Missing user_id")

	user_service.delete_user(user_id)

	return Result.success(msg="User deleted")


