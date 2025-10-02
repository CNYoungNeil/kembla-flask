import json

from app.dto.asanswer_dto import AsanswerDTO
from app.dto.asresult_pdf_dto import AsresultPdfDTO
from app.extensions import db
from app.models.asresult_model import Asresult
from datetime import datetime, UTC, timezone

from app.models.paper_model import Paper
from app.models.ques_option_model import QuesOption
from app.models.question_model import Question
from app.models.user_model import User
from app.utils.answercheck_util import AnswerCheckUtil
from app.utils.pdf_util import PdfUtil
from app.vo.asresult_list_vo import AsresultListVO


class AsresultService:
	# 查询asresult_list列表
	@staticmethod
	def fuzzy_page(dto):
		# 1. 构造查询（关联 user 和 paper）
		query = db.session.query(Asresult, User, Paper) \
			.join(User, Asresult.user_id == User.user_id) \
			.join(Paper, Asresult.paper_id == Paper.paper_id)

		# 2. 条件过滤
		if dto.name:
			query = query.filter(User.name.like(f"%{dto.name}%"))
		if dto.site:
			query = query.filter(User.site.like(f"%{dto.site}%"))
		if dto.status is not None:
			query = query.filter(Asresult.status == dto.status)
		if dto.paperId:
			query = query.filter(Asresult.paper_id == dto.paperId)
		if dto.beginDate:
			query = query.filter(Asresult.submit_time >= dto.beginDate)
		if dto.endDate:
			query = query.filter(Asresult.submit_time <= dto.endDate)

		# 3. 分页
		total = query.count()

		records = query.order_by(Asresult.submit_time.desc()) \
			.offset((dto.pageNum - 1) * dto.pageSize) \
			.limit(dto.pageSize) \
			.all()

		# 4. 封装结果（用 VO）
		result = [AsresultListVO(asr, user, paper).to_dict() for asr, user, paper in records]

		return result, total

	# 添加空记录
	def assign_paper(user_id, paper_id):
		asresult = Asresult(
			user_id=user_id,
			paper_id=paper_id,
			status=2,             # 未开始
			attempt_number=0,    #尝试次数为0
			submit_time=datetime.now(),
		)
		db.session.add(asresult)
		db.session.commit()
		return asresult

	# pdf生成逻辑
	@staticmethod
	def export_pdf(dto: AsresultPdfDTO) -> bytes:
		# 1. 查询数据（复用 fuzzy 查询逻辑，但不分页）
		query = db.session.query(Asresult, User, Paper) \
			.join(User, Asresult.user_id == User.user_id) \
			.join(Paper, Asresult.paper_id == Paper.paper_id)

		fp = dto.filterPage
		if fp.get("name"):
			query = query.filter(User.name.like(f"%{fp['name']}%"))
		if fp.get("status") is not None and fp.get("status") != "":
			query = query.filter(Asresult.status == fp["status"])
		if fp.get("beginDate") and fp.get("endDate"):
			query = query.filter(Asresult.submit_time.between(fp["beginDate"], fp["endDate"]))

		results = query.all()

		# 2. 转成 VO → dict
		vo_list = []
		for asresult, user, paper in results:
			vo = AsresultListVO(asresult, user, paper)
			vo_list.append(vo.to_dict())

		# 3. 调用工具类生成 PDF
		return PdfUtil.generate_pdf(vo_list, dto.selectedFields)

	# 提交答题结果
	@staticmethod
	def submit_with_score(dto: AsanswerDTO):
		"""
		保存答卷并评分
		"""
		# 1. 查找答卷
		asresult = Asresult.query.get(dto.asresultId)
		if not asresult:
			raise Exception("asresult not found")

		# 2. 构造标准答案
		standard_answers = AnswerCheckUtil.build_standard_answers(asresult.paper_id)
		result_map, score, passed = AnswerCheckUtil.compare_answers(dto.answers, standard_answers)

		# 3. 更新原卷（写入答案）
		asresult.answers = json.dumps(dto.answers, ensure_ascii=False)
		asresult.score = score
		asresult.passed = 1 if passed else 0
		asresult.submit_time = datetime.now()
		asresult.duration = dto.duration   # ✅ 保存用时

		# --- 状态流转 ---
		if asresult.attempt_number == 0:  # 第一次提交
			asresult.attempt_number = 1
			if passed:
				asresult.status = 0  # Completed
			else:
				asresult.status = 4  # Failed

				# ⚡ 新建错题卷
				new_asresult = Asresult(
					paper_id=asresult.paper_id,
					user_id=asresult.user_id,
					answers=None,
					score=None,
					passed=0,
					submit_time=datetime.now(),
					attempt_number=2,       # 第二次
					status=3,               # Retry Required
					parent_id=asresult.as_id
				)
				db.session.add(new_asresult)

		elif asresult.attempt_number == 2:  # 第二次提交（错题卷）
			if passed:
				asresult.status = 0  # Completed
			else:
				asresult.status = 4  # Failed

		db.session.commit()

		# 4. 返回结果
		vo_list = []
		for key, is_correct in result_map.items():
			vo_list.append({
				"questionKey": key,
				"userAnswer": dto.answers.get(key, ""),
				"correctAnswer": standard_answers.get(key, ""),
				"isCorrect": is_correct
			})

		return {
			"asresultId": asresult.as_id,
			"paperId": asresult.paper_id,
			"userId": asresult.user_id,
			"score": asresult.score,
			"passed": asresult.passed,
			"attemptNumber": asresult.attempt_number,
			"status": asresult.status,
			"questionResults": vo_list
		}

	# 查看结果
	@staticmethod
	def get_result_by_id(asresult_id: int):
		"""根据 asresultId 查已有答卷结果，只展示用户答过的题"""
		asresult = db.session.query(Asresult).filter_by(as_id=asresult_id).first()
		if not asresult:
			return None

		# paper、user
		paper = db.session.query(Paper).filter_by(paper_id=asresult.paper_id).first()
		user = db.session.query(User).filter_by(user_id=asresult.user_id).first()

		# 用户答案 JSON
		user_answers = json.loads(asresult.answers) if asresult.answers else {}
		result_questions = []

		# 遍历用户答过的题
		for key, user_ans in user_answers.items():
			# key 形如 "q17"
			order_index = int(key.replace("q", ""))

			# 查题目
			q = db.session.query(Question).filter_by(paper_id=asresult.paper_id, order_index=order_index).first()
			if not q:
				continue

			# 查选项，构造标准答案
			options = db.session.query(QuesOption).filter_by(question_id=q.id).all()
			correct_ans = [opt.value for opt in options if opt.is_correct]

			# ⚡ 新增：把选项列表拼进去
			option_list = [
				{
					"value": opt.value,
					"label": opt.label,
				}
				for opt in options
			]


			# 格式化用户答案
			if isinstance(user_ans, str):
				user_ans = user_ans.split(",") if "," in user_ans else [user_ans]

			# 判定对错
			is_correct = set(user_ans) == set(correct_ans)

			result_questions.append({
				"questionTitle": q.content,
				"userAnswer": user_ans,
				"correctAnswer": correct_ans,
				"options": option_list   # ⚡ 新增字段
			})

		return {
			"title": paper.title if paper else "Unknown Paper",
			"username": user.name if user else "Unknown User",
			"score": asresult.score,
			"passed": asresult.passed,
			"submitTime": asresult.submit_time.strftime("%Y-%m-%d %H:%M:%S"),
			"questions": result_questions
		}



