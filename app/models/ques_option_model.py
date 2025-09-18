# app/models/ques_option_model.py
from app.extensions import db

class QuesOption(db.Model):
	__tablename__ = "ques_option"

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	question_id = db.Column(db.Integer, nullable=False)
	label = db.Column(db.String(255), nullable=False)  # 选项内容
	value = db.Column(db.String(10), nullable=False)   # A / B / C / D
	is_correct = db.Column(db.Boolean, default=False)
	order_index = db.Column(db.Integer, default=0)

	def to_dict(self):
		return {
			"optionId": self.id,
			"questionId": self.question_id,
			"label": self.label,
			"value": self.value,
			"isCorrect": self.is_correct,
			"orderIndex": self.order_index
		}

	def __repr__(self):
		return f"<QuesOption id={self.id}, qid={self.question_id}, value={self.value}, correct={self.is_correct}>"
