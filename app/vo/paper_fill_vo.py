class PaperFillVO:
	def __init__(self, paper_id, title, description, questions):
		self.paperId = paper_id
		self.title = title
		self.description = description
		self.questions = questions  # List[QuestionVO]

	def to_dict(self):
		return {
			"paperId": self.paperId,
			"title": self.title,
			"description": self.description,
			"questions": [q.to_dict() for q in self.questions]
		}
