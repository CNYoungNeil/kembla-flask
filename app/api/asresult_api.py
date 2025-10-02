from flask import Blueprint, request, jsonify, make_response

from app.common.result import Result
from app.dto.asanswer_dto import AsanswerDTO
from app.dto.asresult_list_dto import AsanswerListDTO
from app.dto.asresult_pdf_dto import AsresultPdfDTO
from app.services.asresult_service import AsresultService
from app.services.paper_service import PaperService

bp = Blueprint("asresult", __name__)

# 添加新记录到paperlist(userlist分配试卷）（这里只负责添加记录，不负责生成试卷）
@bp.route("/insert", methods=["POST"])
def insert_asresult():
	data = request.get_json()
	user_id = data.get("userId")
	paper_id = data.get("paperId")

	if not user_id or not paper_id:
		return Result.fail("userId and paperId are required")

	asresult = AsresultService.assign_paper(user_id, paper_id)
	return Result.success(asresult.to_dict())

# 多条件/分页查询
@bp.route("/fuzzyPage", methods=["POST"])
def fuzzy_page():
	# 1. 接收前端参数 → 封装成 DTO
	dto = AsanswerListDTO(request.json)

	# 2. 调用 Service 查询
	result, total = AsresultService.fuzzy_page(dto)

	# 3. 用 Result 封装返回
	return Result.success({
		"list": result,
		"total": total
	})

# 生成pdf（列表+字段筛选）
@bp.route("/exportPdf", methods=["POST"])
def export_pdf():
	data = request.get_json()
	dto = AsresultPdfDTO(
		filter_page=data.get("filterPage", {}),
		selected_fields=data.get("selectedFields", [])
	)

	pdf_bytes = AsresultService.export_pdf(dto)

	response = make_response(pdf_bytes)
	response.headers["Content-Type"] = "application/pdf"
	response.headers["Content-Disposition"] = "inline; filename=export.pdf"
	return response


# 提交试卷答案
@bp.route("/submitWithScore", methods=["POST"])
def submit_with_score():
	data = request.get_json()
	dto = AsanswerDTO.from_dict(data)

	print("DEBUG 接收到的数据:", data)


	try:
		vo = AsresultService.submit_with_score(dto)
		return Result.success(vo)
	except Exception as e:
		return Result.fail(f"Submit failed: {str(e)}")


# 查看答题结果
@bp.route("/resultById", methods=["POST"])
def get_result_by_id():
	asresult_id = request.args.get("asresultId", type=int)
	if not asresult_id:
		return Result.fail("Missing asresultId")

	data = AsresultService.get_result_by_id(asresult_id)
	if not data:
		return Result.fail("Result not found")

	return Result.success(data)