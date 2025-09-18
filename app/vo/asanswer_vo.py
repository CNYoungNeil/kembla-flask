class AsanswerVO:
	def __init__(self, question_id, order_index, content, qtype, required, user_answer, correct_answer, is_correct, options):
		self.questionId = question_id
		self.orderIndex = order_index
		self.content = content
		self.type = qtype
		self.required = required
		self.userAnswer = user_answer
		self.correctAnswer = correct_answer
		self.isCorrect = is_correct
		self.options = options  # List[QuesOptionItem]

	def to_dict(self):
		return {
			"questionId": self.questionId,
			"orderIndex": self.orderIndex,
			"content": self.content,
			"type": self.type,
			"required": self.required,
			"userAnswer": self.userAnswer,
			"correctAnswer": self.correctAnswer,
			"isCorrect": self.isCorrect,
			"options": [o.to_dict() for o in self.options]
		}
