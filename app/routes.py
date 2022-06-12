from app import app, pool, dsphieu, phieu, dsdonhang, donhang
from flask import render_template
from app.forms import PhanCongForm, ChiaTuDong, TestForm, DangKyDonForm, TraCuuThongTinNV, SearchForm
from datetime import date,timedelta
from app.forms import User
from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
    flash
)


@app.route('/thongtinnv', methods=['GET', 'POST'])
def thongtinnv():
    form2 = TraCuuThongTinNV()
    if form2.validate_on_submit():
        cccd = form2.cccd.data

        connection = pool.acquire()
        cursor = connection.cursor()

        cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'DD/MM/YYYY HH24:MI:SS'")

        query = f"select * from NHANVIENBD where CCCD = {cccd}"
        cursor.execute(query)
        kq = cursor.fetchall()

        manv = int(kq[0][0])

        query = f"select TenChucVu from CHUCVU a, NHANVIENBD b where a.MaChucVu = b.MaChucVu and b.MaNhanVien = {manv}"
        cursor.execute(query)
        tencv = cursor.fetchone()

        query = f"select to_char(ngaysinh,'DD/MM/YYYY') from NHANVIENBD where MaNhanVien = {manv}"
        cursor.execute(query)
        ngsinh = cursor.fetchone()

        if (tencv[0] == 'Hành chính'):
            print('NV Hành chinh')
            query = f"""select a.madonhang, c.madk, a.mavandon,b.manhanvien
            from phieudonhang a, NHANVIENBD b, donhangdk c
            where c.manhanvien = b.manhanvien and c.madk = a.madk 
            and b.manhanvien = {manv}"""

            cursor.execute(query)
            lichsuhc = cursor.fetchall()
            return render_template('tracuunv1.html', form=form2, thongtin = kq, chucvu = tencv , ngaysinh = ngsinh, lichsunvhc = lichsuhc)
        else: 
            print('NV Giao hàng')
            query = f"""select a.madonhang, a.mavandon, a.madk, manhanvien
            from phieudonhang a, giaohang b
            where a.mavandon = b.mavandon
            and manhanvien = {manv}"""

            cursor.execute(query)
            lichsugh = cursor.fetchall()
            return render_template('tracuunv2.html', form=form2, thongtin = kq, chucvu = tencv , ngaysinh = ngsinh, lichsunvgh = lichsugh)
        connection.commit()
        pool.release(connection)

        
    return render_template('tracuunv.html', form=form2)

@app.route('/phancongcalam', methods=['GET', 'POST'])
def phancongcalam():
    form2 = PhanCongForm()
    if form2.validate_on_submit():
        entrydate = form2.entrydate.data
        thoigian = entrydate.strftime('%d/%m/%Y')
        thoigian = "'" + thoigian +"'"

        ca = form2.ca.data
        manv = form2.manv.data
        connection = pool.acquire()
        cursor = connection.cursor()
        query = f"insert into PHANCONGCALAM values ({manv},{ca},to_date({thoigian},'DD/MM/YYYY'))"
        cursor.execute(query)

        # cursor.callproc('TuDongPhanChiaGiaoHangTheoCa',[2])

        connection.commit()
        pool.release(connection)

    connection = pool.acquire()
    cursor = connection.cursor()
    connection.commit()

    # Lay cac ngay trong tuan hien tai
    today = date.today()
    mon = today - timedelta(days=today.weekday())
    tue = mon + timedelta(days=1)
    wed = mon + timedelta(days=2)
    thu = mon + timedelta(days=3)
    fri = mon + timedelta(days=4)
    # print("Today: " + str(today))
    # print("Mon: " + str(mon))
    # print("Tue: " + str(tue))
    # print("Wed: " + str(wed))
    # print("Thu: " + str(thu))
    # print("Fri: " + str(fri))

    t2 = mon.strftime('%d/%m/%Y')
    chuoit2 = "'" + t2 +"'"
    
    t3 = tue.strftime('%d/%m/%Y')
    chuoit3 = "'" + t3 +"'"

    t4 = wed.strftime('%d/%m/%Y')
    chuoit4 = "'" + t4 +"'"

    t5 = thu.strftime('%d/%m/%Y')
    chuoit5 = "'" + t5 +"'"

    t6 = fri.strftime('%d/%m/%Y')
    chuoit6 = "'" + t6 +"'"

    # Cac ma nhan vien ca 1
    cursor.execute(f"select * from table (Func_MaNhanVienDuocPhanCong ({chuoit2},1))")
    t2ca1 = cursor.fetchall()

    cursor.execute(f"select * from table (Func_MaNhanVienDuocPhanCong ({chuoit3},1))")
    t3ca1 = cursor.fetchall()

    cursor.execute(f"select * from table (Func_MaNhanVienDuocPhanCong ({chuoit4},1))")
    t4ca1 = cursor.fetchall()

    cursor.execute(f"select * from table (Func_MaNhanVienDuocPhanCong ({chuoit5},1))")
    t5ca1 = cursor.fetchall()

    cursor.execute(f"select * from table (Func_MaNhanVienDuocPhanCong ({chuoit6},1))")
    t6ca1 = cursor.fetchall()

    # Cac ma nhan vien ca 2
    cursor.execute(f"select * from table (Func_MaNhanVienDuocPhanCong ({chuoit2},2))")   
    t2ca2 = cursor.fetchall()

    cursor.execute(f"select * from table (Func_MaNhanVienDuocPhanCong ({chuoit3},2))")
    t3ca2 = cursor.fetchall()

    cursor.execute(f"select * from table (Func_MaNhanVienDuocPhanCong ({chuoit4},2))")
    t4ca2 = cursor.fetchall()

    cursor.execute(f"select * from table (Func_MaNhanVienDuocPhanCong ({chuoit5},2))")
    t5ca2 = cursor.fetchall()

    cursor.execute(f"select * from table (Func_MaNhanVienDuocPhanCong ({chuoit6},2))")
    t6ca2 = cursor.fetchall()

    connection.commit()
    pool.release(connection)

    form3 = ChiaTuDong()
    if form3.validate_on_submit():
        connection = pool.acquire()
        cursor = connection.cursor()

        cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'DD/MM/YYYY HH24:MI:SS'")

        cursor.callproc('TuDongPhanChiaGiaoHangTheoCa',[2])
        # cursor.execute("begin TuDongPhanChiaGiaoHangTheoCa(:1); end;", [2])
        connection.commit()
        pool.release(connection)
    return render_template('phancongcalam.html', form=form2, formtd = form3,
    ngayt2 = t2, ngayt3 = t3, ngayt4 = t4, ngayt5 = t5, ngayt6 = t6,
    manvt2ca1 = t2ca1, manvt3ca1 = t3ca1, manvt4ca1 = t4ca1, manvt5ca1 = t5ca1, manvt6ca1 = t6ca1,
    manvt2ca2 = t2ca2, manvt3ca2 = t3ca2, manvt4ca2 = t4ca2, manvt5ca2 = t5ca2, manvt6ca2 = t6ca2)

@app.route('/')
def init():
    return render_template('base.html')

@app.route('/home')
def index():
    return render_template('profile.html')

@app.route('/get')
def get():
    connection = pool.acquire()
    cursor = connection.cursor()
    cursor.execute("select * from KHACHHANG_T")
    r = cursor.fetchall()
    pool.release(connection)
    return str(r)


@app.route('/dangkydonhang', methods=['GET', 'POST'])
def dkdh():
    form2 = DangKyDonForm()
    if form2.validate_on_submit():
        cccd = form2.cccd.data
        tenkh = form2.tenkh.data
        dc_kh = form2.dc_kh.data
        sdt = form2.sdt.data
        dc_gui = form2.dc_gui.data
        dc_nhan = form2.dc_nhan.data
        ghichu = form2.ghichu.data
        mota = form2.mota.data
        dai = form2.dai.data
        rong = form2.rong.data
        cao = form2.cao.data
        kl = form2.kl.data
        ml = form2.ml.data
        cod = form2.cod.data
        tennn = form2.tennn.data
        sdt_nn = form2.sdt_nn.data
        connection = pool.acquire()
        cursor = connection.cursor()
        query = """call dangky_donhang(:cccd,:tenkh,:dc_kh,:sdt,:dc_gui,:dc_nhan,:ghichu,:mota,:dai,:rong,:cao,:kl,:ml,:cod,:tennn,:sdt_nn,:manv)"""
        if cccd == "":
            query = """call dangky_donhang(null,:tenkh,:dc_kh,:sdt,:dc_gui,:dc_nhan,:ghichu,:mota,:dai,:rong,:cao,:kl,:ml,:cod,:tennn,:sdt_nn,:manv)"""
            cursor.execute(query, [tenkh, dc_kh, sdt, dc_gui, dc_nhan,ghichu, mota,dai,rong,cao,kl,ml,cod,tennn,sdt_nn, 1])
        else:
            cursor.execute(query, [cccd, tenkh, dc_kh, sdt, dc_gui, dc_nhan,ghichu, mota,dai,rong,cao,kl,ml,cod,tennn,sdt_nn, 1])
        
        # 2 là số lượng đơn hàng tối đa mà mỗi ngày shipper được giao (tự quy định)
        cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'DD/MM/YYYY HH24:MI:SS'")
        return_val = cursor.callfunc("Func_NgayGiaoNhanhNhat", int, [2])
        chuoi = 'Đơn hàng sẽ được giao nhanh nhất trong vòng ' + str(return_val) + ' ngày'

        connection.commit()
        pool.release(connection)
    
        flash('Dang ky don hang thanh cong')
        flash(chuoi)
        return redirect(url_for('dkdh'))
    return render_template('dangkydonhang.html', form=form2)

@app.route('/donhangtaibd', methods=['GET','POST'])
def dhtbd():
    form2 = SearchForm()
    if form2.validate_on_submit():
        mvd = form2.mavandon.data
        if len(dsdonhang) != 0:
            dsdonhang.pop(0)
        connection = pool.acquire()
        cursor = connection.cursor()
        query = """select tsh.mavandon, bd.trangthai, tsh.phivanchuyen, bd.thoigian
                from thongsohang tsh inner join donhangtaibd bd
                on tsh.mavandon = bd.mavandon
                where tsh.mavandon = :mavandon"""
        cursor.execute(query,[mvd])
        r = cursor.fetchone()
        donhang['mavandon'] = r[0]
        donhang['trangthai'] = r[1]
        donhang['phivanchuyen'] = r[2]
        donhang['thoigian'] = r[3]
        dsdonhang.append(donhang)
        pool.release(connection)
        return redirect(url_for('dhtbd'))
    return render_template('tracuu.html', form=form2, dsdonhang=dsdonhang)

@app.route('/xuatphieu', methods=['GET', 'POST'])
def xuatphieu():
    form2 = SearchForm()
    if form2.validate_on_submit():
        mvd = form2.mavandon.data
        if len(dsphieu) != 0:
            dsphieu.pop(0)
        connection = pool.acquire()
        cursor = connection.cursor()
        query = """select p.madonhang, p.mavandon, p.tennguoinhan, p.sdtnhan, d.thoigiandat, d.diachigui, d.diachinhan, d.motasp, k.tenkhachhang, k.sdt
    from phieudonhang p inner join donhangdk d
    on p.madk = d.madk inner join khachhang k
    on d.makhachhang = k.makhachhang
    where mavandon = :mavandon"""
        cursor.execute(query,[mvd])
        r = cursor.fetchone()
        phieu['madonhang'] = r[0]
        phieu['mavandon'] = r[1]
        phieu['tennguoigui'] = r[8]
        phieu['sdtgui'] = r[9]
        phieu['dcgui'] = r[5]
        phieu['tennguoinhan'] = r[2]
        phieu['sdtnhan'] = r[3]
        phieu['dcnhan'] = r[6]
        phieu['mota'] = r[7]
        phieu['thoigiandat'] = r[4]
        dsphieu.append(phieu)
        pool.release(connection)
        return redirect(url_for('xuatphieu'))
    return render_template('xuatphieu.html', form=form2, dsphieu=dsphieu) 

users = []
users.append(User(id=1, username='nhuvdk', password='qlbd'))
users.append(User(id=2, username='loibt', password='qlbd'))
users.append(User(id=3, username='linhvt', password='qlbd'))
users.append(User(id=3, username='tienttm', password='qlbd'))

@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user
        

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']
        
        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('profile'))

        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/profile')
def profile():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('profile.html')

