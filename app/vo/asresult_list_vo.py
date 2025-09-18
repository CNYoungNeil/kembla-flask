class AsresultListVO:
	def __init__(self, asr, user, paper):
		# Asresult 表
		self.asresultId = asr.as_id
		self.paperId = asr.paper_id
		self.userId = asr.user_id
		self.score = asr.score
		self.passed = asr.passed
		self.status = asr.status
		self.attemptNumber = asr.attempt_number
		self.submitTime = asr.submit_time.strftime("%Y-%m-%d %H:%M:%S") if asr.submit_time else None

		# User 表
		self.roleId = user.role_id if user else None
		self.account = user.account if user else None
		self.username = user.name if user else None
		self.identityId = user.identity_id if user else None
		self.cname = user.cname if user else None
		self.email = user.email if user else None
		self.site = user.site if user else None

		# Paper 表
		self.title = paper.title if paper else None
		self.description = paper.description if paper else None

	def to_dict(self):
		return self.__dict__
