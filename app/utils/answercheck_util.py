from app.models.question_model import Question
from app.models.ques_option_model import QuesOption

class AnswerCheckUtil:

	@staticmethod
	def build_standard_answers(paper_id):
		"""生成标准答案字典：{ 'q1': 'A', 'q2': 'B,C' }"""
		standard = {}
		questions = Question.query.filter_by(paper_id=paper_id).all()
		for q in questions:
			options = QuesOption.query.filter_by(question_id=q.id).all()
			correct_values = [opt.value for opt in options if opt.is_correct]
			standard[f"q{q.order_index}"] = ",".join(sorted(correct_values))  # 多选用逗号拼接
		return standard


	@staticmethod
	def compare_answers(user_answers: dict, standard_answers: dict):
		"""
		比对用户答案和标准答案
		返回: (result_map, score, passed)
		"""
		result_map = {}
		correct_count = 0

		for key, correct in standard_answers.items():
			user_ans = user_answers.get(key, "")
			normalized = ",".join(sorted(user_ans.split(","))) if user_ans else ""
			is_correct = (normalized == correct)
			result_map[key] = is_correct
			if is_correct:
				correct_count += 1

		# ✅ 用用户提交的题目数量作为总数
		current_count = len(user_answers)
		total_count = len(standard_answers)
		score = int(correct_count / total_count * 100) if total_count > 0 else 0
		passed = (current_count > 0 and correct_count == current_count)  # 必须有题且全对才算通过

		# 👉 打印调试信息
		print("DEBUG:", "current_count=", current_count, "correct_count=", correct_count, "score=", score, "passed=", passed)

		return result_map, score, passed


