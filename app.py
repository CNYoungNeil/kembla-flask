from flask import Flask, request, jsonify  # send_from_directory 暂时不用
from flask_cors import CORS
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError
import os, sys
import config
import socket

from app.extensions import db, jwt
from app.api.user_api import bp as user_bp
from app.api.paper_api import bp as paper_bp
from app.api.asresult_api import bp as asresult_bp

# -------------------------------
# 🔹 开发模式（CORS 跨域, 不托管前端）
# -------------------------------
# '''
app = Flask(__name__)   # 👉 static_folder / static_url_path 去掉
app.config.from_object(config)

# 启用 CORS：允许 Vue 开发服务器 (8080) 访问
CORS(app, resources={r"/*": {"origins": "*"}})

db.init_app(app)
jwt.init_app(app)
# '''


# 注册蓝图
app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(paper_bp, url_prefix="/paper")
app.register_blueprint(asresult_bp, url_prefix="/asresult")

# 白名单，不需要校验 token 的路径
WHITE_LIST = ["/user/login"]

@app.before_request
def global_jwt_check():
    if request.path.startswith(("/user", "/paper", "/asresult")) and request.path not in WHITE_LIST:
        try:
            verify_jwt_in_request()
        except NoAuthorizationError:
            return jsonify({"msg": "Missing Authorization Header"}), 401
        except Exception as e:
            return jsonify({"msg": f"Token error: {str(e)}"}), 401


# 检查端口是否被占用（避免多开）
def check_port_in_use(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0

# 退出接口
@app.route('/exit', methods=['GET'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        os._exit(0)
    func()
    return "✅ Server shutting down..."


# ---------------------------------------------------
# 🔹 打包模式 (EXE 一键启动 + Vue 静态资源托管)
# 👉 打包时需要把下面注释取消
# ---------------------------------------------------
"""
from flask import send_from_directory

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_vue(path):
    static_folder = "app/static_frontend"
    full_path = os.path.join(static_folder, path)

    # 如果请求是 API 路径，直接返回 404
    if path.startswith(("user", "paper", "asresult")):
        return jsonify({"msg": "Not Found"}), 404

    # 静态文件存在，直接返回
    if path != "" and os.path.exists(full_path):
        print(f"[STATIC] Serving file: {path}")
        return send_from_directory(static_folder, path)

    # 兜底交给 Vue Router
    print(f"[VUE] Serving index.html for path: {path}")
    return send_from_directory(static_folder, "index.html")
"""


if __name__ == '__main__':
    host, port = "127.0.0.1", 8090

    # 避免多开
    if check_port_in_use(host, port):
        print(f"⚠️ Port {port} already in use, exiting.")
        sys.exit(0)

    # ---------------------------------------------------
    # 🔹 打包模式 (EXE 自动打开前端页面)
    # 👉 打包时需要把下面注释取消
    # ---------------------------------------------------
    """
    import webbrowser
    url = f"http://{host}:{port}"
    webbrowser.open(url)
    """

    app.run(host=host, port=port, debug=True, use_reloader=False)   # use_reloader为热部署开关
