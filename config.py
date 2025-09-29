import urllib.parse

# 数据库配置
DB_HOST = "BI-SQL04\\SYSPRO"   # 主机+实例名
DB_NAME = "kembla_admin"
DB_USER = "kembla"
DB_PASSWORD = "kembla"

# Flask/JWT 密钥
SECRET_KEY = "kemblapj-secretkey-flask"        # Flask 内部用的
JWT_SECRET_KEY = "kemblapj-secretkey-jwt"    # 专门给 JWT 用的

DB_PASSWORD = urllib.parse.quote(DB_PASSWORD)

# PDF 导出配置
PDF_FONT_NAME = "Arial"   # 英文字体直接用系统自带的 Arial
PDF_FONT_SIZE = 10

# 使用 pyodbc 驱动
SQLALCHEMY_DATABASE_URI = (
	f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
	"?driver=ODBC+Driver+17+for+SQL+Server"
)

SQLALCHEMY_TRACK_MODIFICATIONS = False
