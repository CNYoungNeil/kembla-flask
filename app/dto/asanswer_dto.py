# app/dto/asanswer_dto.py
from typing import Dict, Any

class AsanswerDTO:
	def __init__(self, asresult_id=None, user_id=None, paper_id=None, duration=None, answers=None):
		self.asresultId = asresult_id
		self.userId = user_id
		self.paperId = paper_id
		self.answers = answers or {}   # {"q1":"A", "q2":"B,C", ...}
		self.duration = duration

	@classmethod
	def from_dict(cls, data: Dict[str, Any]):
		return cls(
			asresult_id=data.get("asresultId"),
			user_id=data.get("userId"),
			paper_id=data.get("paperId"),
			answers=data.get("answers"),
			duration=data.get("duration"),  # ✅ 要加这个
		)
