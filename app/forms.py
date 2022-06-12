from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, DateField, StringField
from wtforms.validators import DataRequired

class PhanCongForm(FlaskForm):
    entrydate = DateField('Ngày', validators=[DataRequired()])
    manv = IntegerField('Mã Nhân Viên', validators=[DataRequired()])
    ca = IntegerField('Ca số', validators=[DataRequired()])
    submit = SubmitField(label='Xác Nhận')

class ChiaTuDong(FlaskForm):
    nutTuDong = SubmitField(label='TuDongPhanChia')

class TraCuuThongTinNV(FlaskForm):
    manv = StringField('Mã Nhân Viên', validators=[DataRequired()])
    nutTraCuuNV = SubmitField(label='TraCuuNV')

class TraCuuThongTinKH(FlaskForm):
    makh = StringField('Mã Khách Hàng', validators=[DataRequired()])
    nutTraCuuKH = SubmitField(label='TraCuuKH')

class TraCuuThongTinAllKH(FlaskForm):
    ToanBoKH = SubmitField(label='TraCuuToanBoKH')

class TestForm(FlaskForm):
    makh = IntegerField(label='Mã Khách Hàng', validators=[DataRequired()])
    tenkh = StringField(label='Tên Khách Hàng', validators=[DataRequired()])
    diachi = StringField(label='Địa Chỉ', validators=[DataRequired()])
    sdt = StringField(label='Số Điện Thoại', validators=[DataRequired()])
    LoaiKH = StringField(label='Loại Khách Hàng', validators=[DataRequired()])
    
    # stringfield
    submit = SubmitField(label='Xác Nhận')

class DangKyDonForm(FlaskForm):
    makh = IntegerField(label='Mã Khách Hàng', default=-1)
    tenkh = StringField('Tên Người Gửi', validators=[DataRequired()])
    sdt = StringField('Số Điện Thoại Người Gửi', validators=[DataRequired()])
    dc_kh = StringField('Địa Chỉ Khách Hàng', validators=[DataRequired()])
    dc_gui = StringField('Địa Chỉ Gửi', validators=[DataRequired()])
    dc_nhan = StringField('Địa Chỉ Nhận', validators=[DataRequired()])
    ghichu = StringField('Ghi Chú')
    mota = StringField('Mô Tả')
    dai = IntegerField(label='Chiều Dài')
    rong = IntegerField(label='Chiều Rộng')
    cao = IntegerField(label='Chiều Cao')
    kl = IntegerField(label='Khối Lượng')
    ml = IntegerField(label='Mã Loại')
    cod = IntegerField(label='COD')
    tennn = StringField('Tên Người Nhận', validators=[DataRequired()])
    cccd = StringField('Căn Cước Công Dân (CCCD)', validators=[DataRequired()])
    sdt_nn = StringField('Số Điện Thoại Người Nhận', validators=[DataRequired()])
    submit = SubmitField('Xác Nhận')

class SearchForm(FlaskForm):
    mavandon = StringField(label='Mã Vận Đơn', validators=[DataRequired()]) 
    submit = SubmitField('Xác Nhận')

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

# users = []
# users.append(User(id=1, username='nhuvdk', password='qlbd'))
# users.append(User(id=2, username='loibt', password='qlbd'))
# users.append(User(id=3, username='linhvt', password='qlbd'))
# users.append(User(id=3, username='tienttm', password='qlbd'))