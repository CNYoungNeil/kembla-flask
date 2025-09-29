from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError
import os
import config   # ✅ 改为直接导入模块，保证打包能找到
import socket


from app.extensions import db, jwt
from app.api.user_api import bp as user_bp
from app.api.paper_api import bp as paper_bp
from app.api.asresult_api import bp as asresult_bp

app = Flask(
    __name__,
    static_folder="app/static_frontend",  # ✅ Vue 打包后的目录
    static_url_path="/"                   # ✅ 修改这里：把 "" 改成 "/"，避免 js/css 路径找不到
)
app.config.from_object(config)

# 启用 CORS（如果只用 exe，可以改成 "*"）
CORS(app, resources={r"/*": {"origins": "*"}})

db.init_app(app)
jwt.init_app(app)

# 蓝图注册
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



# 检查端口是否已被占用（避免多开）
def check_port_in_use(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0
# 退出进程
@app.route('/exit', methods=['GET'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        os._exit(0)
    func()
    return "✅ Server shutting down..."


# 前端 Vue 页面托管
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_vue(path):
    static_folder = app.static_folder
    full_path = os.path.join(static_folder, path)

    # 👉 如果请求是 API 路径，直接返回 404（交给蓝图去处理）
    if path.startswith(("user", "paper", "asresult")):
        return jsonify({"msg": "Not Found"}), 404

    # 👉 静态资源文件存在，直接返回
    if path != "" and os.path.exists(full_path):
        print(f"[STATIC] Serving file: {path}")
        return send_from_directory(static_folder, path)

    # 👉 其它情况兜底交给 Vue Router
    print(f"[VUE] Serving index.html for path: {path}")
    return send_from_directory(static_folder, "index.html")


if __name__ == '__main__':
    host, port = "127.0.0.1", 8090

    # 👉 避免多开
    if check_port_in_use(host, port):
        print(f"⚠️ Port {port} already in use, exiting.")
        sys.exit(0)

    import webbrowser
    url = f"http://{host}:{port}"
    webbrowser.open(url)
    app.run(host=host, port=port, debug=False)

