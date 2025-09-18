from fpdf import FPDF

class PdfUtil:

	@staticmethod
	def generate_pdf(data_list: list[dict], selected_fields: list[str]) -> bytes:
		pdf = FPDF(orientation="L", unit="mm", format="A4")
		pdf.add_page()

		pdf.set_auto_page_break(auto=True, margin=15)
		pdf.set_margins(left=15, top=20, right=15)

		# 标题
		pdf.set_font("Arial", "B", 16)
		pdf.cell(0, 10, "Assessment List", ln=True, align="C")
		pdf.ln(8)

		if not data_list:
			pdf.set_font("Arial", size=10)
			pdf.cell(200, 10, "No data available", ln=True, align="C")
			return bytes(pdf.output(dest="S"))

		# ---------- 计算列宽 ----------
		pdf.set_font("Arial", size=9)
		max_widths = {"No.": 10}
		max_widths.update({field: pdf.get_string_width(field) + 6 for field in selected_fields})

		for row in data_list:
			for field in selected_fields:
				text = str(row.get(field, ""))
				text_width = pdf.get_string_width(text) + 6
				if text_width > max_widths[field]:
					max_widths[field] = text_width

		# ---------- 调整列宽，填满整页 ----------
		page_width = pdf.w - 30   # 减去左右边距
		total_width = sum(max_widths.values())
		if total_width < page_width:
			scale = page_width / total_width
			for field in max_widths:
				max_widths[field] *= scale

		# ---------- 表头 ----------
		pdf.set_font("Arial", "B", 9)
		pdf.set_x((pdf.w - sum(max_widths.values())) / 2)
		pdf.cell(max_widths["No."], 10, "No.", border=1, align="C")
		for field in selected_fields:
			pdf.cell(max_widths[field], 10, field, border=1, align="C")
		pdf.ln()

		# ---------- 表内容 ----------
		pdf.set_font("Arial", size=9)
		row_index = 1
		for row in data_list:
			pdf.set_x((pdf.w - sum(max_widths.values())) / 2)
			pdf.cell(max_widths["No."], 8, str(row_index), border=1, align="C")
			row_index += 1
			for field in selected_fields:
				text = str(row.get(field, ""))
				col_width = max_widths[field]

				# 保证单行 fit，不截断
				if pdf.get_string_width(text) > col_width - 2:
					pdf.set_font("Arial", size=7)  # 缩小字体
					pdf.cell(col_width, 8, text, border=1, align="C")
					pdf.set_font("Arial", size=9)
				else:
					pdf.cell(col_width, 8, text, border=1, align="C")
			pdf.ln()

		return bytes(pdf.output(dest="S"))
