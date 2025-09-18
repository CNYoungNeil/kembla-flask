# app/dto/asanswer_list_dto.py
from datetime import date

class AsanswerListDTO:
	def __init__(self, data: dict):
		"""
		data: 前端传来的 JSON 字典
		"""
		self.userId = data.get("userId")
		self.userRoleId = data.get("userRoleId")

		self.paperId = data.get("paperId")
		self.name = data.get("name")
		self.filterRoleId = data.get("filterRoleId")
		self.site = data.get("site")
		self.status = data.get("status")

		self.beginDate = data.get("beginDate")  # 建议存字符串，后面转 datetime
		self.endDate = data.get("endDate")

		self.pageNum = int(data.get("pageNum", 1))
		self.pageSize = int(data.get("pageSize", 10))

	def to_dict(self):
		return {
			"userId": self.userId,
			"userRoleId": self.userRoleId,
			"paperId": self.paperId,
			"name": self.name,
			"filterRoleId": self.filterRoleId,
			"site": self.site,
			"status": self.status,
			"beginDate": self.beginDate,
			"endDate": self.endDate,
			"pageNum": self.pageNum,
			"pageSize": self.pageSize,
		}
