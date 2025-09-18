class QuesOptionItem:
	def __init__(self, option_id, value, label):
		self.optionId = option_id
		self.value = value   # 选项 A/B/C/D
		self.label = label   # 选项文字描述

	def to_dict(self):
		return {
			"optionId": self.optionId,
			"value": self.value,
			"label": self.label
		}
