from flask import Blueprint, request

from app.common.result import Result
from app.services.paper_service import PaperService

bp = Blueprint("paper", __name__)

# 试卷本体列表展示查询
@bp.route("listAll")
def listAll():
	list_paper = PaperService.listAll()
	return Result.success(list_paper)   #变量名不重要，前端始终用res.data.data拿数据

# # 获取新的空试卷
# @bp.route("/<int:paper_id>/full", methods=["GET"])
# def get_full_paper(paper_id):
# 	paper = PaperService.get_full_paper(paper_id)
# 	return Result.success(paper)

# 生成答题空试卷（新卷/错题卷）
@bp.route("/fill", methods=["GET"])
def fill_paper():
	asresult_id = request.args.get("asresultId", type=int)
	if not asresult_id:
		return Result.fail("缺少参数 asresultId")

	paper_data = PaperService.get_paper_by_asresult(asresult_id)
	if not paper_data:
		return Result.fail("试卷加载失败或状态不正确")

	return Result.success(paper_data)