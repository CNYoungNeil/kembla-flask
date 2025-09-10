from app.extensions import db

class User(db.Model):
	__tablename__ = "users"

	user_id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
	account = db.Column("account", db.String(32), nullable=False, unique=True)
	name = db.Column("name", db.String(32), nullable=False)
	identity_id = db.Column("identity_id", db.String(32))
	password = db.Column("password", db.String(128), nullable=False)
	cname = db.Column("cname", db.String(32))
	sex = db.Column("sex", db.String(4))
	phone = db.Column("phone", db.String(16))
	email = db.Column("email", db.String(64))
	role_id = db.Column("role_id", db.Integer)
	con_email = db.Column("con_email", db.String(64))
	site = db.Column("site", db.String(128))
	is_valid = db.Column("is_valid", db.Boolean, default=True)

	def to_dict(self):
		return {
			"userId": self.user_id,
			"account": self.account,
			"name": self.name,
			"identityId": self.identity_id,
			"cname": self.cname,
			"sex": self.sex,
			"phone": self.phone,
			"email": self.email,
			"roleId": self.role_id,
			"conEmail": self.con_email,
			"site": self.site,
			"isValid": self.is_valid,
		}

	def __repr__(self):
		# 获取所有字段和值
		fields = {attr.key: getattr(self, attr.key) for attr in self.__mapper__.attrs}
		return f"<User {fields}>"
