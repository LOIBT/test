from flask import Flask
from key import config
import cx_Oracle

pool = cx_Oracle.SessionPool(user=config['oracle_user'], password=config['oracle_passwd'], dsn=config['DSN'], min=3, max=3, increment=0, getmode=cx_Oracle.SPOOL_ATTRVAL_WAIT, encoding="UTF-8")

app = Flask(__name__)
app.config['SECRET_KEY'] = config['skey']

dsphieu = []
phieu = {
    'madonhang': '',
    'mavandon': '',
    'tennguoigui': '',
    'sdtgui': '',
    'dcgui': '',
    'tennguoinhan': '',
    'sdtnhan': '',
    'dcnhan': '',
    'mota': '',
    'thoigiandat': ''
}

dsthongsohang = []
thongsohang = {
    'mavandon': '',
    'dai' : '',
    'rong' : '',
    'cao' : '',
    'khoiluong' :'',
    'mankl' : '',
    'maloai' : '',
    'phivanchuyen' : '',
    'cod' : ''
}

dsdonhang = []
donhang = {
    'mavandon': '',
    'trangthai': '',
    'phivanchuyen': -1,
    'thoigian': ''
}

from app import routes
