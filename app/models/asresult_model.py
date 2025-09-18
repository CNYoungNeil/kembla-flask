from app.extensions import db
from datetime import datetime

class Asresult(db.Model):
	__tablename__ = "asresult"

	as_id = db.Column("id",db.Integer, primary_key=True, autoincrement=True)
	paper_id = db.Column(db.Integer, nullable=False)
	user_id = db.Column(db.Integer, nullable=False)
	answers = db.Column(db.Text)   # 对应 nvarchar(max)
	score = db.Column(db.Integer)
	passed = db.Column(db.Boolean)  # bit 映射为 Boolean
	submit_time = db.Column(db.DateTime, default=datetime.utcnow)
	attempt_number = db.Column(db.Integer)
	status = db.Column(db.Integer)   # 0=Completed, 1=In Progress, 2=Not Started, 3=Draft
	parent_id = db.Column(db.BigInteger)

	def to_dict(self):
		return {
			"asId": self.as_id,
			"paperId": self.paper_id,
			"userId": self.user_id,
			"answers": self.answers,
			"score": self.score,
			"passed": self.passed,
			"submitTime": self.submit_time.isoformat() if self.submit_time else None,
			"attemptNumber": self.attempt_number,
			"status": self.status,
			"parentId": self.parent_id,
		}

	def __repr__(self):
		fields = {attr.key: getattr(self, attr.key) for attr in self.__mapper__.attrs}
		return f"<Asresult {fields}>"
