from flask import Blueprint

from app.common.result import Result
from app.services import paper_service

bp = Blueprint("paper", __name__)

@bp.route("listAll")
def listAll():
	list_paper = paper_service.listAll()
	return Result.success(list_paper)   #变量名不重要，前端始终用res.data.data拿数据