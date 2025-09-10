from datetime import datetime

from app.extensions import db
from app.models.user_model import User

def authenticate(account, password):
	"""
	校验账号和密码
	"""
	user = User.query.filter_by(account=account).first()
	if user and user.password == password:   # 明文对比
		return user
	return None


# 条件分页查询
def get_user_list(name, account, identity_id, page_num, page_size):
	query = User.query

	if name:
		query = query.filter(User.name.like(f"%{name}%"))
	if account:
		query = query.filter(User.account.like(f"%{account}%"))
	if identity_id:
		query = query.filter(User.identity_id.like(f"%{identity_id}%"))

	# ✅ 必须加一个 order_by，MSSQL 要求
	query = query.order_by(User.user_id)

	pagination = query.paginate(page=page_num, per_page=page_size, error_out=False)
	records = [u.to_dict() for u in pagination.items]

	return {
		"list": records,
		"total": pagination.total,
		"pageNum": page_num,
		"pageSize": page_size
	}

# 创建用户（表单提交）
def create_user(data: dict) -> User:

	# 手动生成 identity_id
	identity_id = generate_identity_id(data.get("roleId"))

	new_user = User(
		account=data.get("account"),
		name=data.get("name"),
		password=data.get("password"),
		cname=data.get("cname"),
		sex=data.get("sex"),
		phone=data.get("phone"),
		email=data.get("email"),
		role_id=data.get("roleId"),
		con_email=data.get("conEmail"),
		site=data.get("site"),
		is_valid=True,
		identity_id=identity_id
	)

	db.session.add(new_user)
	db.session.commit()

	return new_user

# 删除用户
def delete_user(user_id: int) -> bool:
	user = User.query.get(user_id)
	if not user:
		return False

	db.session.delete(user)
	db.session.commit()
	return True


# 工具方法：生成identity_id
def generate_identity_id(role_id: int) -> str:
	# 1. 前缀 = 角色前两个字母大写
	prefix = "RO" + str(role_id)

	# 2. 日期 = ddMMyyyy
	date_str = datetime.now().strftime("%d%m%Y")

	# 3. 查已有数量
	like_pattern = f"{prefix}{date_str}%"
	count = User.query.filter(User.identity_id.like(like_pattern)).count()

	# 4. 序号 = 已有数量 + 1，补齐3位
	serial = str(count + 1).zfill(4)

	return f"{prefix}{date_str}{serial}"