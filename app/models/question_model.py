from app.extensions import db

class Question(db.Model):
	__tablename__ = "question"

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	paper_id = db.Column(db.Integer, nullable=False)
	content = db.Column(db.Text, nullable=False)
	type = db.Column(db.String(20), nullable=False)
	order_index = db.Column(db.Integer, nullable=False)
	required = db.Column(db.Boolean, default=True)  # bit → Boolean

	def to_dict(self):
		return {
			"questionId": self.id,
			"paperId": self.paper_id,
			"content": self.content,
			"type": self.type,
			"orderIndex": self.order_index,
			"required": bool(self.required)   # 转成 True/False，前端更好处理
		}
