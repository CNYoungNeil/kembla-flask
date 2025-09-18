class QuestionItem:
	def __init__(self, question_id, order_index, content, qtype, required, options):
		self.questionId = question_id
		self.orderIndex = order_index
		self.content = content
		self.type = qtype       # single / multi
		self.required = required
		self.options = options  # List[QuesOptionVO]

	def to_dict(self):
		return {
			"questionId": self.questionId,
			"orderIndex": self.orderIndex,
			"content": self.content,
			"type": self.type,
			"required": self.required,
			"options": [o.to_dict() for o in self.options]
		}
