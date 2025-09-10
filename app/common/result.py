from flask import jsonify

class Result:
	@staticmethod
	def success(data=None, msg="success"):
		return jsonify({
			"code": 1,
			"msg": msg,
			"data": data
		})

	@staticmethod
	def fail(msg="fail", code=0):
		return jsonify({
			"code": code,
			"msg": msg,
			"data": None
		})
