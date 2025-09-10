from app.extensions import db
from datetime import datetime

class Paper(db.Model):
	__tablename__ = "paper"

	paper_id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
	title = db.Column("title", db.String(100), nullable=False)
	description = db.Column("description", db.Text)
	role_type = db.Column("role_type", db.String(50))
	create_time = db.Column("create_time", db.DateTime, default=datetime.utcnow)

	def to_dict(self):
		return {
			"paperId": self.paper_id,
			"title": self.title,
			"description": self.description,
			"roleType": self.role_type,
			"createTime": self.create_time.strftime("%Y-%m-%d %H:%M:%S") if self.create_time else None
		}

	def __repr__(self):
		fields = {attr.key: getattr(self, attr.key) for attr in self.__mapper__.attrs}
		return f"<Paper {fields}>"
