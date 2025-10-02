import json

from app.extensions import db
from app.item.ques_option_item import QuesOptionItem
from app.models.asresult_model import Asresult
from app.models.paper_model import Paper
from app.models.ques_option_model import QuesOption
from app.models.question_model import Question
from app.item.question_item import QuestionItem
from app.utils.answercheck_util import AnswerCheckUtil

from app.vo.paper_fill_vo import PaperFillVO


class PaperService:

	# 试卷原卷列表
	@staticmethod
	def listAll():
		list_paper = Paper.query.all()
		return [p.to_dict() for p in list_paper]



	# 生成新试卷/错题卷
	@staticmethod
	def get_paper_by_asresult(asresult_id: int):
		"""根据 asresultId 生成试卷（新卷=整卷 / 错题卷=只返回错题）"""
		asresult = Asresult.query.get(asresult_id)
		if not asresult:
			return None

		# 查询该卷所有题目
		questions = Question.query.filter_by(paper_id=asresult.paper_id).all()

		    # 取 Paper 信息
		paper = Paper.query.get(asresult.paper_id)
		if not paper:
			return None

		# ---- 新卷：status = 2 → 返回整卷 ----
		if asresult.status == 2:
			# 第一次进入试卷，初始化 attemptNumber = 0
			if not asresult.attempt_number:
				asresult.attempt_number = 0
				db.session.commit()

			question_items = []
			for q in questions:
				options = QuesOption.query.filter_by(question_id=q.id).all()
				option_items = [QuesOptionItem(opt.id, opt.value, opt.label) for opt in options]
				question_items.append(
					QuestionItem(q.id, q.order_index, q.content, q.type, q.required, option_items)
				)
			return PaperFillVO(asresult.paper_id, paper.title, paper.description
			, question_items).to_dict()

		# ---- 错题卷：status = 3 → 根据答案筛选错题 ----
		elif asresult.status == 3:
			# ⚠️ 取父卷答案
			parent_asresult = Asresult.query.get(asresult.parent_id)
			user_answers = json.loads(parent_asresult.answers or "{}")

			standard_answers = AnswerCheckUtil.build_standard_answers(asresult.paper_id)

			# 找出错题 key
			wrong_keys = [
				key for key, correct in standard_answers.items()
				if user_answers.get(key, "") != correct
			]

			question_items = []
			for q in questions:
				key = f"q{q.order_index}"
				if key not in wrong_keys:
					continue
				options = QuesOption.query.filter_by(question_id=q.id).all()
				option_items = [QuesOptionItem(opt.id, opt.value, opt.label) for opt in options]
				question_items.append(
					QuestionItem(q.id, q.order_index, q.content, q.type, q.required, option_items)
				)

			return PaperFillVO(
				asresult.paper_id,
				f"{paper.title} (Retry)",   # ✅ 在原始 title 基础上加 Retry
				paper.description,          # ✅ 还是用数据库里的 description
				question_items
			).to_dict()



		# 其他状态
		return "Paper doesn't display properly!"

	@staticmethod
	def add_full_paper(data: dict):
		print("DEBUG received data:", data)
		print("DEBUG type(roleType):", type(data.get("roleType")))

		try:
			# 1. 新建试卷
			paper = Paper(
				title=data["title"],
				description=data.get("description"),
				role_type=data.get("roleType")
			)
			db.session.add(paper)
			db.session.flush()  # 获取 paper_id

			# 2. 新建题目和选项
			for q in data.get("questions", []):
				question = Question(
					paper_id=paper.paper_id,
					content=q.get("content"),
					type=q.get("type"),
					order_index=q.get("orderIndex"),  # ✅ 没有就 None → NULL
					required=q.get("required", True)
				)

				db.session.add(question)
				db.session.flush()

				for opt in q.get("options", []):
					option = QuesOption(
						question_id=question.id,
						label=opt["label"],
						value=opt["value"],
						order_index=opt.get("orderIndex"),
						is_correct=opt.get("isCorrect", False)
					)

					db.session.add(option)

			db.session.commit()
			return {"paperId": paper.paper_id}
		except Exception as e:
			db.session.rollback()
			raise e

		