# asresult_pdf_dto.py
# 点击“pdf生成”按钮之后传的内容
class AsresultPdfDTO:
	def __init__(self, filter_page: dict, selected_fields: list[str]):
		"""
		:param filter_page: 筛选条件（复用 AsresultListDTO 的结构，不包含 pageNum/pageSize）
		:param selected_fields: 前端勾选的字段名列表，例如 ["Name", "Email", "Score"]
		"""
		self.filterPage = filter_page
		self.selectedFields = selected_fields
