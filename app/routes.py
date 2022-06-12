from app import app, pool, dsphieu, phieu, dsdonhang, donhang, dsthongsohang, thongsohang
from flask import render_template
from app.forms import PhanCongForm, DangKyDonForm, TraCuuThongTinNV, SearchForm, TraCuuThongTinKH, TraCuuThongTinAllKH
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

@app.route('/thongtinkh', methods=['GET', 'POST'])
def thongtinkh():
    form = TraCuuThongTinKH()

    connection = pool.acquire()
    cursor = connection.cursor()

    query1 = "select * from KHACHHANG"

    cursor.execute(query1)
    kq1 = cursor.fetchall()
    if form.validate_on_submit():
            makh = form.makh.data

            connection = pool.acquire()
            cursor = connection.cursor()

            query = f" select * from KHACHHANG where MaKhachHang = {makh}"

            cursor.execute(query)
            kq = cursor.fetchall()

            connection.commit()
            pool.release(connection)

            return render_template('tracuukh1.html',formmakh=form,kh=kq, kh1=kq1)
    connection.commit()
    pool.release(connection)
    return render_template('tracuukh.html', formmakh=form, kh1=kq1)

@app.route('/thongtinnv', methods=['GET', 'POST'])
def thongtinnv():
    form2 = TraCuuThongTinNV()
    query1 = """select MaNhanVien,Email,TenNhanVien,SDT,DiaChi,CCCD,TenChucVu,to_char(ngaysinh,'DD/MM/YYYY') 
    from NHANVIENBD a, CHUCVU b where a.MaChucVu = b.MaChucVu """

    connection = pool.acquire()
    cursor = connection.cursor()

    cursor.execute(query1)
    kq1 = cursor.fetchall()
    if form2.validate_on_submit():
        manv = form2.manv.data

        cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'DD/MM/YYYY HH24:MI:SS'")

        query = f"select * from NHANVIENBD where MaNhanVien = {manv}"
        cursor.execute(query)
        kq = cursor.fetchall()

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
            connection.commit()
            pool.release(connection)

            return render_template('tracuunv1.html', form=form2, nv=kq1,
            thongtin = kq, chucvu = tencv , ngaysinh = ngsinh, lichsunvhc = lichsuhc)
        else: 
            print('NV Giao hàng')
            query = f"""select a.madonhang, a.mavandon, a.madk, manhanvien
            from phieudonhang a, giaohang b
            where a.mavandon = b.mavandon
            and manhanvien = {manv}"""

            cursor.execute(query)
            lichsugh = cursor.fetchall()

            connection.commit()
            pool.release(connection)

            return render_template('tracuunv2.html', form=form2, nv=kq1,
            thongtin = kq, chucvu = tencv , ngaysinh = ngsinh, lichsunvgh = lichsugh)
    return render_template('tracuunv.html', form=form2 , nv=kq1)

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

        connection.commit()
        pool.release(connection)

        return redirect(url_for('phancongcalam'))
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

    # Ma nhan vien giao hang ca 1
    cursor.execute(f"select distinct manv,tennv from table (Func_MaNhanVienGHDuocPhanCong ({chuoit2},1))")
    manvght2ca1 = cursor.fetchall()

    cursor.execute(f"select distinct manv,tennv from table (Func_MaNhanVienGHDuocPhanCong ({chuoit3},1))")
    manvght3ca1 = cursor.fetchall()

    cursor.execute(f"select distinct manv,tennv from table (Func_MaNhanVienGHDuocPhanCong ({chuoit4},1))")
    manvght4ca1 = cursor.fetchall()

    cursor.execute(f"select distinct manv,tennv from table (Func_MaNhanVienGHDuocPhanCong ({chuoit5},1))")
    manvght5ca1 = cursor.fetchall()

    cursor.execute(f"select distinct manv,tennv from table (Func_MaNhanVienGHDuocPhanCong ({chuoit6},1))")
    manvght6ca1 = cursor.fetchall()

    # Ma nhan vien hanh chinh ca 1
    cursor.execute(f"select distinct manv,tennv from table (Func_MaNhanVienHCDuocPhanCong ({chuoit2},1))")
    manvhct2ca1 = cursor.fetchall()

    cursor.execute(f"select distinct manv,tennv from table (Func_MaNhanVienHCDuocPhanCong ({chuoit3},1))")
    manvhct3ca1 = cursor.fetchall()

    cursor.execute(f"select distinct manv,tennv from table (Func_MaNhanVienHCDuocPhanCong ({chuoit4},1))")
    manvhct4ca1 = cursor.fetchall()

    cursor.execute(f"select distinct manv,tennv from table (Func_MaNhanVienHCDuocPhanCong ({chuoit5},1))")
    manvhct5ca1 = cursor.fetchall()

    cursor.execute(f"select distinct manv,tennv from table (Func_MaNhanVienHCDuocPhanCong ({chuoit6},1))")
    manvhct6ca1 = cursor.fetchall()

    # Ma nhan vien giao hang ca 2
    cursor.execute(f"select distinct manv,tennv from table (Func_MaNhanVienGHDuocPhanCong ({chuoit2},2))")
    manvght2ca2 = cursor.fetchall()

    cursor.execute(f"select distinct manv,tennv from table (Func_MaNhanVienGHDuocPhanCong ({chuoit3},2))")
    manvght3ca2 = cursor.fetchall()

    cursor.execute(f"select distinct manv,tennv from table (Func_MaNhanVienGHDuocPhanCong ({chuoit4},2))")
    manvght4ca2 = cursor.fetchall()

    cursor.execute(f"select distinct manv,tennv from table (Func_MaNhanVienGHDuocPhanCong ({chuoit5},2))")
    manvght5ca2 = cursor.fetchall()

    cursor.execute(f"select distinct manv,tennv from table (Func_MaNhanVienGHDuocPhanCong ({chuoit6},2))")
    manvght6ca2 = cursor.fetchall()

    # Ma nhan vien hanh chinh ca 2
    cursor.execute(f"select distinct manv,tennv from table (Func_MaNhanVienHCDuocPhanCong ({chuoit2},2))")
    manvhct2ca2 = cursor.fetchall()

    cursor.execute(f"select distinct manv,tennv from table (Func_MaNhanVienHCDuocPhanCong ({chuoit3},2))")
    manvhct3ca2 = cursor.fetchall()

    cursor.execute(f"select distinct manv,tennv from table (Func_MaNhanVienHCDuocPhanCong ({chuoit4},2))")
    manvhct4ca2 = cursor.fetchall()

    cursor.execute(f"select distinct manv,tennv from table (Func_MaNhanVienHCDuocPhanCong ({chuoit5},2))")
    manvhct5ca2 = cursor.fetchall()

    cursor.execute(f"select distinct manv,tennv from table (Func_MaNhanVienHCDuocPhanCong ({chuoit6},2))")
    manvhct6ca2 = cursor.fetchall()

    # So nhan vien giao hàng ca 1
    cursor.execute(f"select COUNT(distinct manv) from table (Func_MaNhanVienGHDuocPhanCong ({chuoit2},1))")
    ght2ca1 = cursor.fetchall()

    cursor.execute(f"select COUNT(distinct manv) from table (Func_MaNhanVienGHDuocPhanCong ({chuoit3},1))")
    ght3ca1 = cursor.fetchall()

    cursor.execute(f"select COUNT(distinct manv) from table (Func_MaNhanVienGHDuocPhanCong ({chuoit4},1))")
    ght4ca1 = cursor.fetchall()

    cursor.execute(f"select COUNT(distinct manv) from table (Func_MaNhanVienGHDuocPhanCong ({chuoit5},1))")
    ght5ca1 = cursor.fetchall()

    cursor.execute(f"select COUNT(distinct manv) from table (Func_MaNhanVienGHDuocPhanCong ({chuoit6},1))")
    ght6ca1 = cursor.fetchall()

    # So nhan vien hanh chinh ca 1
    cursor.execute(f"select COUNT(distinct manv) from table (Func_MaNhanVienHCDuocPhanCong ({chuoit2},1))")
    hct2ca1 = cursor.fetchall()

    cursor.execute(f"select COUNT(distinct manv) from table (Func_MaNhanVienHCDuocPhanCong ({chuoit3},1))")
    hct3ca1 = cursor.fetchall()

    cursor.execute(f"select COUNT(distinct manv) from table (Func_MaNhanVienHCDuocPhanCong ({chuoit4},1))")
    hct4ca1 = cursor.fetchall()

    cursor.execute(f"select COUNT(distinct manv) from table (Func_MaNhanVienHCDuocPhanCong ({chuoit5},1))")
    hct5ca1 = cursor.fetchall()

    cursor.execute(f"select COUNT(distinct manv) from table (Func_MaNhanVienHCDuocPhanCong ({chuoit6},1))")
    hct6ca1 = cursor.fetchall()

    # So nhan vien giao hang ca 2
    cursor.execute(f"select COUNT(distinct manv) from table (Func_MaNhanVienGHDuocPhanCong ({chuoit2},2))")   
    ght2ca2 = cursor.fetchall()

    cursor.execute(f"select COUNT(distinct manv) from table (Func_MaNhanVienGHDuocPhanCong ({chuoit3},2))")
    ght3ca2 = cursor.fetchall()

    cursor.execute(f"select COUNT(distinct manv) from table (Func_MaNhanVienGHDuocPhanCong ({chuoit4},2))")
    ght4ca2 = cursor.fetchall()

    cursor.execute(f"select COUNT(distinct manv) from table (Func_MaNhanVienGHDuocPhanCong ({chuoit5},2))")
    ght5ca2 = cursor.fetchall()

    cursor.execute(f"select COUNT(distinct manv) from table (Func_MaNhanVienGHDuocPhanCong ({chuoit6},2))")
    ght6ca2 = cursor.fetchall()

    # So nhan vien hanh chinh ca 2
    cursor.execute(f"select COUNT(distinct manv) from table (Func_MaNhanVienHCDuocPhanCong ({chuoit2},2))")   
    hct2ca2 = cursor.fetchall()

    cursor.execute(f"select COUNT(distinct manv) from table (Func_MaNhanVienHCDuocPhanCong ({chuoit3},2))")
    hct3ca2 = cursor.fetchall()

    cursor.execute(f"select COUNT(distinct manv) from table (Func_MaNhanVienHCDuocPhanCong ({chuoit4},2))")
    hct4ca2 = cursor.fetchall()

    cursor.execute(f"select COUNT(distinct manv) from table (Func_MaNhanVienHCDuocPhanCong ({chuoit5},2))")
    hct5ca2 = cursor.fetchall()

    cursor.execute(f"select COUNT(distinct manv) from table (Func_MaNhanVienHCDuocPhanCong ({chuoit6},2))")
    hct6ca2 = cursor.fetchall()

    connection.commit()
    pool.release(connection)

    # form3 = ChiaTuDong()
    # if form3.validate_on_submit():
    #     connection = pool.acquire()
    #     cursor = connection.cursor()

    #     cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'DD/MM/YYYY HH24:MI:SS'")

    #     cursor.callproc('TuDongPhanChiaGiaoHangTheoCa',[2])
        
    #     connection.commit()
    #     pool.release(connection)
    return render_template('phancongcalam.html', form=form2,
    ngayt2 = t2, ngayt3 = t3, ngayt4 = t4, ngayt5 = t5, ngayt6 = t6,
    slght2ca1 = ght2ca1, slght3ca1 = ght3ca1, slght4ca1 = ght4ca1, slght5ca1 = ght5ca1, slght6ca1 = ght6ca1,
    slhct2ca1 = hct2ca1, slhct3ca1 = hct3ca1, slhct4ca1 = hct4ca1, slhct5ca1 = hct5ca1, slhct6ca1 = hct6ca1,
    slght2ca2 = ght2ca2, slght3ca2 = ght3ca2, slght4ca2 = ght4ca2, slght5ca2 = ght5ca2, slght6ca2 = ght6ca2,
    slhct2ca2 = hct2ca2, slhct3ca2 = hct3ca2, slhct4ca2 = hct4ca2, slhct5ca2 = hct5ca2, slhct6ca2 = hct6ca2,
    manvght2ca1 = manvght2ca1,manvght3ca1 = manvght3ca1,manvght4ca1 = manvght4ca1,manvght5ca1 = manvght5ca1,manvght6ca1 = manvght6ca1,
    manvhct2ca1 = manvhct2ca1,manvhct3ca1 = manvhct3ca1,manvhct4ca1 = manvhct4ca1,manvhct5ca1 = manvhct5ca1,manvhct6ca1 = manvhct6ca1,
    manvght2ca2 = manvght2ca2,manvght3ca2 = manvght3ca2,manvght4ca2 = manvght4ca2,manvght5ca2 = manvght5ca2,manvght6ca2 = manvght6ca2,
    manvhct2ca2 = manvhct2ca2,manvhct3ca2 = manvhct3ca2,manvhct4ca2 = manvhct4ca2,manvhct5ca2 = manvhct5ca2,manvhct6ca2 = manvhct6ca2)

@app.route('/')
def init():
    return render_template('base.html')

@app.route('/phanconggiaohang')
def phanconggiaohang():
    today = date.today()

    homnay = today.strftime('%d/%m/%Y')

    connection = pool.acquire()
    cursor = connection.cursor()

    cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'DD/MM/YYYY HH24:MI:SS'")

    cursor.callproc('Proc_ChayKtraPCGiaoHang')

    query = f"""select MaNhanVien,MaVanDon,ThoiGian 
    from GIAOHANG, dual
    where to_char(THOIGIAN,'DD/MM/YYYY') = to_char(sysdate,'DD/MM/YYYY') """

    cursor.execute(query)
    kq = cursor.fetchall()

    connection.commit()
    pool.release(connection)
    
    return render_template('phanconggiaohang.html',giaohang=kq, homnay = homnay)

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
        chuoi = 'Đơn hàng sẽ được giao nhanh nhất trong vòng ' + str(return_val+1) + ' ngày'

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

        connection = pool.acquire()
        cursor = connection.cursor()

        # Xuat phieu don hang
        if len(dsphieu) != 0:
            dsphieu.pop(0)

        query = """select p.madonhang, p.mavandon, p.tennguoinhan, p.sdtnhan, to_char(d.thoigiandat,'DD/MM/YYYY'), d.diachigui, d.diachinhan, d.motasp, k.tenkhachhang, k.sdt
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

        # Thong so hang
        if len(dsthongsohang) != 0:
            thongsohang.pop(0)

        query = """select mavandon, dai, rong, cao, khoiluong, mankl, maloai, phivanchuyen, cod
        from thongsohang where mavandon = :mavandon"""
        cursor.execute(query,[mvd])
        kq = cursor.fetchone()

        thongsohang['mavandon'] = kq[0]
        thongsohang['dai'] = kq[1]
        thongsohang['rong'] = kq[2]
        thongsohang['cao'] = kq[3]
        thongsohang['khoiluong'] = kq[4]
        thongsohang['mankl'] = kq[5]
        thongsohang['maloai'] = kq[6]
        thongsohang['phivanchuyen'] = kq[7]
        thongsohang['cod'] = kq[8]
        dsthongsohang.append(thongsohang)
        # Trang thai
        if len(dsdonhang) != 0:
            dsdonhang.pop(0)

        query = """select tsh.mavandon, bd.trangthai, tsh.phivanchuyen, bd.thoigian
                from thongsohang tsh inner join donhangtaibd bd
                on tsh.mavandon = bd.mavandon
                where tsh.mavandon = :mavandon"""
        cursor.execute(query,[mvd])
        t = cursor.fetchone()

        donhang['mavandon'] = t[0]
        donhang['trangthai'] = t[1]
        donhang['phivanchuyen'] = t[2]
        donhang['thoigian'] = t[3]
        dsdonhang.append(donhang)

        pool.release(connection)
        return redirect(url_for('xuatphieu'))
    return render_template('xuatphieu.html', form=form2,
    dsphieu=dsphieu , dsdonhang=dsdonhang , dsthongsohang=dsthongsohang ) 

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

