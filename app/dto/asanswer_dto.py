# app/dto/asanswer_dto.py
from typing import Dict, Any

class AsanswerDTO:
	def __init__(self, asresult_id=None, user_id=None, paper_id=None, attempt_number=None, answers=None):
		self.asresultId = asresult_id
		self.userId = user_id
		self.paperId = paper_id
		self.answers = answers or {}   # {"q1":"A", "q2":"B,C", ...}

	@classmethod
	def from_dict(cls, data: Dict[str, Any]):
		return cls(
			asresult_id=data.get("asresultId"),
			user_id=data.get("userId"),
			paper_id=data.get("paperId"),
			answers=data.get("answers"),
		)
