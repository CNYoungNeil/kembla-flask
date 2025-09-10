from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError

from app.extensions import db, jwt
from app.api.user_api import bp as user_bp
from app.api.paper_api import bp as paper_bp

app = Flask(__name__)
app.config.from_object("config")

# 启用 CORS，处理跨域的问题
CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})

db.init_app(app)
jwt.init_app(app)

# 蓝图注册
app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(paper_bp, url_prefix="/paper")

# 白名单，不需要校验 token 的路径
WHITE_LIST = [
	"/user/login",   # 登录接口
]


@app.before_request
def global_jwt_check():
	# 跳过白名单
	if request.path in WHITE_LIST:
		return

	try:
		verify_jwt_in_request()  # 会自动解析 Authorization: Bearer xxx
	except NoAuthorizationError:
		return jsonify({"msg": "Missing Authorization Header"}), 401
	except Exception as e:
		return jsonify({"msg": f"Token error: {str(e)}"}), 401


if __name__ == '__main__':
	app.run(host="127.0.0.1", port=8090, debug=True)
