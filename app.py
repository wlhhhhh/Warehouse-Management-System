from flask_bootstrap import Bootstrap
from flask_datepicker import datepicker
from flask import Flask, render_template, request, url_for, flash, redirect, jsonify
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, FloatField, DateField, PasswordField, BooleanField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

import os


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
bootstrap = Bootstrap(app)
moment = Moment(app)


app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:@localhost/tpc-h'
app.config["SQLALCHEMY_COMMENT_ON_TEARDOWN"] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
app.config['WTF_CSRF_SECRET_KEY'] = 'wlh'
app.secret_key = 'wlh'

db = SQLAlchemy(app)


class Part(db.Model):
    __tablename__ = 'PART'
    P_PARTKEY = db.Column(db.Integer, primary_key=True)
    P_NAME = db.Column(db.String(55))
    P_MFGR = db.Column(db.String(25))
    P_BRAND = db.Column(db.String(10))
    P_TYPE = db.Column(db.String(25))
    P_SIZE = db.Column(db.Integer)
    P_CONTAINER = db.Column(db.String(10))
    P_RETAILPRICE = db.Column(db.Float)
    P_COMMENT = db.Column(db.String(23))


class Region(db.Model):
    __tablename__ = 'REGION'
    R_REGIONKEY = db.Column(db.Integer, primary_key=True)
    R_NAME = db.Column(db.String(25))
    R_COMMENT = db.Column(db.String(152))
    PS_SUPPLYCOST = db.Column(db.Float)
    PS_COMMENT = db.Column(db.String(199))


class Nation(db.Model):
    __tablename__ = 'NATION'
    N_NATIONKEY = db.Column(db.Integer, primary_key=True)
    N_NAME = db.Column(db.String(25))
    N_REGIONKEY = db.Column(db.Integer, db.ForeignKey('REGION.R_REGIONKEY'))
    N_COMMENT = db.Column(db.String(152))
    reg = db.relationship("Region", backref="find_name")


class Customer(db.Model):
    __tablename__ = 'CUSTOMER'
    C_CUSTKEY = db.Column(db.Integer, primary_key=True)
    C_NAME = db.Column(db.String(25))
    C_ADDRESS = db.Column(db.String(40))
    C_NATIONKEY = db.Column(db.Integer, db.ForeignKey('NATION.N_NATIONKEY'))
    C_PHONE = db.Column(db.String(16))
    C_ACCTBAL = db.Column(db.Float)
    C_MKTSEGMENT = db.Column(db.String(10))
    C_COMMENT = db.Column(db.String(117))
    NAT = db.relationship("Nation", backref="cfind_name")


class Supplier(db.Model):
    __tablename__ = 'SUPPLIER'
    S_SUPPKEY = db.Column(db.Integer, primary_key=True)
    S_NAME = db.Column(db.String(25))
    S_ADDRESS = db.Column(db.String(40))
    S_NATIONKEY = db.Column(db.Integer, db.ForeignKey('NATION.N_NATIONKEY'))
    S_PHONE = db.Column(db.String(15))
    S_ACCTBAL = db.Column(db.Float)
    S_COMMENT = db.Column(db.String(101))
    nati = db.relationship("Nation", backref="sfind_name")


class Partsupp(db.Model):
    __tablename__ = 'PARTSUPP'
    PS_PARTKEY = db.Column(db.Integer, db.ForeignKey('PART.P_PARTKEY'), primary_key=True)
    PS_SUPPKEY = db.Column(db.Integer, db.ForeignKey('SUPPLIER.S_SUPPKEY'), primary_key=True)
    PS_AVAILQTY = db.Column(db.Integer)
    PS_SUPPLYCOST = db.Column(db.Float)
    PS_COMMENT = db.Column(db.String(199))


class Orders(db.Model):
    __tablename__ = 'ORDERS'
    O_ORDERKEY = db.Column(db.Integer, primary_key=True)
    O_CUSTKEY = db.Column(db.Integer, db.ForeignKey('CUSTOMER.C_CUSTKEY'))
    O_ORDERSTATUS = db.Column(db.String(1))
    O_TOTALPRICE = db.Column(db.Float)
    O_ORDERDATE = db.Column(db.Date)
    O_ORDERPRIORITY = db.Column(db.String(15))
    O_CLERK = db.Column(db.String(15))
    O_SHIPPRIORITY = db.Column(db.Integer)
    O_COMMENT = db.Column(db.String(79))


class Lineitem(db.Model):
    L_ORDERKEY = db.Column(db.Integer, db.ForeignKey('ORDERS.O_ORDERKEY'), primary_key=True)
    L_PARTKEY = db.Column(db.Integer, db.ForeignKey('PARTSUPP.PS_PARTKEY'), db.ForeignKey('PARTSUPP.PS_SUPPKEY'))
    L_SUPPKEY = db.Column(db.Integer, db.ForeignKey('PARTSUPP.PS_PARTKEY'), db.ForeignKey('PARTSUPP.PS_SUPPKEY'))
    L_LINENUMBER = db.Column(db.Integer, primary_key=True)
    L_QUANTITY = db.Column(db.Float)
    L_EXTENDEDPRICE = db.Column(db.Float)
    L_DISCOUNT = db.Column(db.Float)
    L_TAX = db.Column(db.Float)
    L_RETURNFLAG = db.Column(db.String(1))
    L_LINESTATUS = db.Column(db.String(1))
    L_SHIPDATE = db.Column(db.Date)
    L_COMMITDATE = db.Column(db.Date)
    L_RECEIPTDATE = db.Column(db.Date)
    L_SHIPINSTRUCT = db.Column(db.String(25))
    L_SHIPMODE = db.Column(db.String(25))
    L_COMMENT = db.Column(db.String(44))


'''class Role(db.Model):
    __table__ = 'ROLES'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return '<Role %r>' % self.name'''


class User(db.Model):
    __tablename__ = 'USERS'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, index=True)
    password = db.Column(db.String(128), unique=True, index=True)

    def __repr__(self):
        return '<User %r>' % self.username


db.create_all()


class Select(SelectField):
    def pre_validate(self, form):
        pass


class EditFormPart(FlaskForm):
    part_key = IntegerField('????????????', validators=[])
    name = StringField('????????????', validators=[])
    MFGR = StringField('MFGR', validators=[])
    brand = SelectField('??????', validators=[], render_kw={'class': 'form-control'},
                        choices=[('??????', '??????'), ('??????', '??????'), ('??????', '??????'),
                                 ('??????', '??????'), ('??????', '??????'), ('??????', '??????'),
                                 ('TE', 'TE')],
                        default='TE', coerce=str)
    type = SelectField('??????', validators=[], render_kw={'class': 'form-control'},
                        choices=[('????????????', '????????????'), ('????????????', '????????????'),
                                ('????????????', '????????????')], default='????????????', coerce=str)
    size = IntegerField('??????', validators=[])
    container = SelectField('????????????', validators=[], render_kw={'class': 'form-control'},
                            choices=[('???????????????', '???????????????'), ('????????????', '????????????')],
                            default='????????????', coerce=str)
    retailprice = FloatField('?????????', validators=[])
    comment = StringField('??????', validators=[])
    submit = SubmitField('??????')


class EditFormRegion(FlaskForm):
    regionkey = IntegerField('????????????', validators=[])
    regionname = StringField('????????????', validators=[])
    r_comment = StringField('??????', validators=[])
    supplycost = FloatField('????????????', validators=[])
    ps_comment = StringField('??????(??????)', validators=[])
    submit = SubmitField('??????')


class EditFormNation(FlaskForm):
    nationkey = IntegerField('????????????', validators=[])
    nationname = StringField('????????????', validators=[])
    '''region = []
    regions = Region.query.order_by(Region.R_NAME).all()
    for i in regions:
        region.append((i.R_REGIONKEY, i.R_NAME))
    n_regionkey = SelectField('????????????', validators=[], render_kw={'class': 'form-control'}, coerce=int)'''
    n_regionkey = Select('????????????', validators=[], render_kw={'class': 'form-control'}, choices=[(0, '???')],
                              coerce=int)
    comment = StringField('??????', validators=[])
    submit = SubmitField('??????')


def UpdateFormNation():
    EditFormNation.nationkey = IntegerField('????????????', validators=[])
    EditFormNation.nationname = StringField('????????????', validators=[])
    region = []
    regions = Region.query.order_by(Region.R_NAME).all()
    for i in regions:
        region.append((i.R_REGIONKEY, '(%d)'%i.R_REGIONKEY + i.R_NAME))
    EditFormNation.n_regionkey = Select('????????????', validators=[], render_kw={'class': 'form-control'},
                                           choices=region, coerce=int)
    EditFormNation.n_regionkey.choices += region
    EditFormNation.comment = StringField('??????', validators=[])
    EditFormNation.submit = SubmitField('??????')
    return


class EditFormCustomer(FlaskForm):
    custkey = IntegerField('????????????', validators=[])
    name = StringField('????????????', validators=[])
    address = StringField('????????????', validators=[])
    nation = []
    nations = Nation.query.all()
    for i in nations:
        nation.append((i.N_NATIONKEY, i.N_NAME))
    c_nationkey = Select('????????????', validators=[], render_kw={'class':'form-control'}, choices=nation, coerce=int)
    phone = StringField('????????????', validators=[])
    acctbal = FloatField('????????????', validators=[])
    mktsegment = StringField('??????', validators=[])
    comment = StringField('??????', validators=[])
    submit = SubmitField('??????')


def UpdateFormCustomer():
    EditFormCustomer.custkey = IntegerField('????????????', validators=[])
    EditFormCustomer.name = StringField('????????????', validators=[])
    EditFormCustomer.address = StringField('????????????', validators=[])
    nation = []
    nations = Nation.query.all()
    for i in nations:
        nation.append((i.N_NATIONKEY, i.N_NAME))
    EditFormCustomer.c_nationkey = Select('????????????', validators=[], render_kw={'class': 'form-control'}, choices=nation, coerce=int)
    EditFormCustomer.phone = StringField('????????????', validators=[])
    EditFormCustomer.acctbal = FloatField('????????????', validators=[])
    EditFormCustomer.mktsegment = StringField('??????', validators=[])
    EditFormCustomer.comment = StringField('??????', validators=[])
    EditFormCustomer.submit = SubmitField('??????')
    return


class EditFormSupplier(FlaskForm):
    suppkey = IntegerField('???????????????', validators=[])
    name = StringField('???????????????', validators=[])
    address = StringField('???????????????', validators=[])
    nation = []
    nations = Nation.query.all()
    for i in nations:
        nation.append((i.N_NATIONKEY, '(%d)'%i.N_NATIONKEY + i.N_NAME))
    nationkey = Select('????????????', validators=[], render_kw={'class': 'form-control'}, choices=nation, coerce=int)
    phone = StringField('??????', validators=[])
    acctbal = FloatField('????????????', validators=[])
    comment = StringField('??????', validators=[])
    submit = SubmitField('??????')


def UpdateFormSupplier():
    EditFormSupplier.suppkey = IntegerField('???????????????', validators=[])
    EditFormSupplier.name = StringField('???????????????', validators=[])
    EditFormSupplier.address = StringField('???????????????', validators=[])
    nation = []
    nations = Nation.query.all()
    for i in nations:
        nation.append((i.N_NATIONKEY, '(%d)'%i.N_NATIONKEY + i.N_NAME))
    EditFormSupplier.nationkey = Select('????????????', validators=[], render_kw={'class': 'form-control'}, choices=nation, coerce=int)
    EditFormSupplier.phone = StringField('??????', validators=[])
    EditFormSupplier.acctbal = FloatField('????????????', validators=[])
    EditFormSupplier.comment = StringField('??????', validators=[])
    EditFormSupplier.submit = SubmitField('??????')
    return


class EditFormPartsupp(FlaskForm):
    part = []
    parts = Part.query.all()
    for i in parts:
        part.append((i.P_PARTKEY, '(%d)'%i.P_PARTKEY + i.P_NAME))
    partkey = Select('????????????', validators=[], render_kw={'class':'form-control'}, choices=part, coerce=int)
    supplier = []
    suppliers = Supplier.query.all()
    for i in suppliers:
        supplier.append((i.S_SUPPKEY, '(%d)'%i.S_SUPPKEY + i.S_NAME))
    suppkey = Select('???????????????', validators=[], render_kw={'class':'form-control'}, choices=supplier, coerce=int)
    availqty = IntegerField('????????????', validators=[])
    supplycost = FloatField('????????????', validators=[])
    comment = StringField('??????', validators=[])
    submit = SubmitField('??????')


def UpdateFormPartsupp():
    part = []
    parts = Part.query.all()
    for i in parts:
        part.append((i.P_PARTKEY, '(%d)'%i.P_PARTKEY + i.P_NAME))
    EditFormPartsupp.partkey = Select('????????????', validators=[], render_kw={'class': 'form-control'}, choices=part, coerce=int)
    supplier = []
    suppliers = Supplier.query.all()
    for i in suppliers:
        supplier.append((i.S_SUPPKEY, '(%d)'%i.S_SUPPKEY + i.S_NAME))
    EditFormPartsupp.suppkey = Select('???????????????', validators=[], render_kw={'class': 'form-control'}, choices=supplier, coerce=int)
    EditFormPartsupp.availqty = IntegerField('????????????', validators=[])
    EditFormPartsupp.supplycost = FloatField('????????????', validators=[])
    EditFormPartsupp.comment = StringField('??????', validators=[])
    EditFormPartsupp.submit = SubmitField('??????')


class EditFormOrders(FlaskForm):
    orderkey = IntegerField('????????????', validators=[])
    customer = []
    customers = Customer.query.all()
    for i in customers:
        customer.append((i.C_CUSTKEY, '(%d)'%i.C_CUSTKEY + i.C_NAME))
    custkey = SelectField('????????????', validators=[], render_kw={'class':'form-control'}, choices=customer, coerce=int)
    orderstatus = Select('????????????', validators=[],
                         render_kw={'class':'form-control'},
                         choices={("?????????", "?????????"), ("?????????", '?????????'), ("?????????", "?????????")}, default='', coerce=str)
    '''totalprice = FloatField('????????????', validators=[])'''
    orderdate = DateField('????????????', default='', render_kw={'id':'date'}, format='%Y-%m-%d')
    orderpriority = StringField('?????????', validators=[])
    clerk = StringField('?????????', validators=[])
    shippriority = IntegerField('???????????????', validators=[])
    comment = StringField('??????', validators=[])
    submit = SubmitField('??????')


def UpdateFormOrders():
    EditFormOrders.orderkey = IntegerField('????????????', validators=[])
    customer = []
    customers = Customer.query.all()
    for i in customers:
        customer.append((i.C_CUSTKEY, '(%d)'%i.C_CUSTKEY + i.C_NAME))
    EditFormOrders.custkey = Select('????????????', validators=[], render_kw={'class': 'form-control'}, choices=customer, coerce=int)
    EditFormOrders.orderstatus = Select('????????????', validators=[],
                                        render_kw={'class':'form-control'},
                                        choices={("?????????", "?????????"), ("?????????", '?????????'), ("?????????", "?????????")}, default='', coerce=str)
    '''EditFormOrders.totalprice = FloatField('????????????', validators=[])'''
    EditFormOrders.orderdate = DateField('????????????', default='', render_kw={'id':'date'}, format='%Y-%m-%d')
    EditFormOrders.orderpriority = StringField('?????????', validators=[])
    EditFormOrders.clerk = StringField('?????????', validators=[])
    EditFormOrders.shippriority = IntegerField('???????????????', validators=[])
    EditFormOrders.comment = StringField('??????', validators=[])
    EditFormOrders.submit = SubmitField('??????')


class EditFormLineitem(FlaskForm):
    order = []
    orders = Orders.query.all()
    for i in orders:
        order.append((i.O_ORDERKEY, i.O_ORDERKEY))
    orderkey = Select('?????????', validators=[], render_kw={'class': 'form-control'}, choices=order, coerce=int)
    part = []
    parts = Part.query.all()
    for i in parts:
        part.append((i.P_PARTKEY, '(%d)'%i.P_PARTKEY + i.P_NAME))
    partkey = Select('??????', validators=[], render_kw={'class': 'form-control'}, choices=part, coerce=int)
    supplier = []
    suppliers = Supplier.query.all()
    for i in suppliers:
        supplier.append((i.S_SUPPKEY, '(%d)'%i.S_SUPPKEY + i.S_NAME))
    suppkey = Select('?????????', validators=[], render_kw={'class': 'form-control'}, choices=supplier, coerce=int)
    linenumber = IntegerField('????????????', validators=[])
    quantity = FloatField('??????', validators=[])
    '''extendedprice = FloatField('?????????', validators=[])'''
    discount = FloatField('??????', validators=[])
    tax = FloatField('???', validators=[])
    returnflag = Select('????????????', validators=[], render_kw={'class':'form-control'}, choices={('???', '???'), ('???', '???')}, coerce=str)
    linestatus = Select('??????????????????', validators=[],
                        render_kw={'class':'form-control'},
                        choices={("?????????", "?????????"), ("?????????", '?????????'), ("?????????", "?????????")}, default='', coerce=str)
    shipdate = DateField('????????????', default='', validators=[], render_kw={'id':'date'}, format='%Y-%m-%d')
    commitdate = DateField('????????????', default='', validators=[], render_kw={'id':'date1'}, format='%Y-%m-%d')
    receiptdate = DateField('????????????', default='', validators=[], render_kw={'id':'date2'}, format='%Y-%m-%d')
    shipinstruct = StringField('????????????', validators=[])
    shipmode = StringField('????????????', validators=[])
    comment = StringField('??????', validators=[])
    submit = SubmitField('??????')


def UpdateFormLineitem():
    order = []
    orders = Orders.query.all()
    for i in orders:
        order.append((i.O_ORDERKEY, i.O_ORDERKEY))
    EditFormLineitem.orderkey = Select('?????????', validators=[], render_kw={'class': 'form-control'}, choices=order, coerce=int)
    part = []
    parts = Part.query.all()
    for i in parts:
        part.append((i.P_PARTKEY, '(%d)'%i.P_PARTKEY + i.P_NAME))
    EditFormLineitem.partkey = Select('????????????', validators=[], render_kw={'class': 'form-control'}, choices=part, coerce=int)
    supplier = []
    suppliers = Supplier.query.all()
    for i in suppliers:
        supplier.append((i.S_SUPPKEY, '(%d)'%i.S_SUPPKEY + i.S_NAME))
    EditFormLineitem.suppkey = Select('???????????????', validators=[], render_kw={'class': 'form-control'}, choices=supplier, coerce=int)
    EditFormLineitem.linenumber = IntegerField('????????????', validators=[])
    EditFormLineitem.quantity = FloatField('??????', validators=[])
    '''EditFormLineitem.extendedprice = FloatField('?????????', validators=[])'''
    EditFormLineitem.discount = FloatField('??????', validators=[])
    EditFormLineitem.tax = FloatField('???', validators=[])
    EditFormLineitem.returnflag = Select('????????????', validators=[], render_kw={'class':'form-control'}, choices={('???', '???'), ('???', '???')}, coerce=str)
    EditFormLineitem.linestatus = Select('??????????????????', validators=[],
                                        render_kw={'class':'form-control'},
                                        choices={("?????????", "?????????"), ("?????????", '?????????'), ("?????????", "?????????")}, default=0, coerce=str)
    EditFormLineitem.shipdate = DateField('????????????', default='', validators=[], render_kw={'id':'date'}, format='%Y-%m-%d')
    EditFormLineitem.commitdate = DateField('????????????', default='', validators=[], render_kw={'id':'date1'}, format='%Y-%m-%d')
    EditFormLineitem.receiptdate = DateField('????????????', default='', validators=[], render_kw={'id':'date2'}, format='%Y-%m-%d')
    EditFormLineitem.shipinstruct = StringField('????????????', validators=[])
    EditFormLineitem.shipmode = StringField('????????????', validators=[])
    EditFormLineitem.comment = StringField('??????', validators=[])
    EditFormLineitem.submit = SubmitField('??????')


class SearchForm(FlaskForm):
    part_key = IntegerField('??????', validators=[])
    submit = SubmitField('??????')


class SearchFormforRegion(FlaskForm):
    regionkey = IntegerField('??????', validators=[])
    submit = SubmitField('??????')


class SearchFormforNation(FlaskForm):
    nationkey = IntegerField('??????', validators=[])
    submit = SubmitField('??????')


class SearchFormforCustomer(FlaskForm):
    c_custkey = IntegerField('??????', validators=[])
    submit = SubmitField('??????')


class SearchFormforSupplier(FlaskForm):
    suppkey = IntegerField('??????', validators=[])
    submit = SubmitField('??????')


class SearchFormforPartsupp(FlaskForm):
    partkey = IntegerField('????????????', validators=[])
    suppkey = IntegerField('???????????????', validators=[])
    submit = SubmitField('??????')


class SearchFormforOrders(FlaskForm):
    orderkey = IntegerField('????????????', validators=[])
    submit = SubmitField('??????')


class SearchFormforLineitem(FlaskForm):
    orderkey = IntegerField('????????????', validators=[])
    linenumber = IntegerField('??????????????????', validators=[])
    submit = SubmitField('??????')


''''@app.route('/', methods=['GET', 'POST'])
def login():
    return render_template('logIn_cl.html')'''


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template(('logIn_gm.html'))


@app.route('/login_validation', methods=['GET', 'POST'])
def login_validation():
    users = User.query.all()
    if request.method == 'POST':
        username = request.form['username']
        passwd = request.form['passwd']
        for user in users:
            if user.username == username :
                if user.password == passwd:
                    data = {'username':username, 'passwd':passwd}
                    return jsonify(data)


@app.route('/register_validation', methods=['GET', 'POST'])
def register_validation():
    users = User.query.all()
    id1 = 0
    if request.method == 'POST':
        username = request.form['username']
        passwd = request.form['passwd']
        for user in users:
            id1 = id1 + 1
            if user.username == username:
                data = {False}
                return jsonify(data)
        user = User(id=id1, username=username, password=passwd)
        db.session.add(user)
        data ={'username':username, 'passwd':passwd}
        jsonify(data)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        parts = Part.query.filter_by(P_PARTKEY=form.part_key.data).all()
    else:
        parts = Part.query.all()
    return render_template('part.html', title_name='welcome', parts=parts, form=form)


@app.route('/add_part', methods=['GET', 'POST'])
def add_part():
    form = EditFormPart()
    if form.validate_on_submit():
        try:
            part = Part(P_PARTKEY=form.part_key.data,
                        P_NAME=form.name.data, P_MFGR=form.MFGR.data, P_BRAND=form.brand.data,
                        P_TYPE=form.type.data, P_SIZE=form.size.data, P_CONTAINER=form.container.data,
                        P_RETAILPRICE=form.retailprice.data, P_COMMENT=form.comment.data)
            db.session.add(part)
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            print(e)
            flash("????????????")
            db.session.rollback()
            return render_template('edit_part.html', form=form)
    else:
        return render_template('edit_part.html', form=form)


@app.route('/delete_part/<int:id>', methods=['GET', 'POST'])
def delete_part(id):
    part = Part.query.get(id)
    if part:
        try:
            db.session.delete(part)
            db.session.commit()
            flash("????????????")
        except Exception as e:
            print(e)
            flash("????????????")
            db.session.rollback()
    else:
        flash("???????????????")
    print(url_for('index'))
    return redirect(url_for('index'))


@app.route('/edit_part/<int:id>', methods=['GET', 'POST'])
def edit_part(id):
    part = Part.query.get(id)
    form = EditFormPart(part_key=part.P_PARTKEY, name=part.P_NAME, MFGR=part.P_MFGR,
                        brand=part.P_BRAND, type=part.P_TYPE, size=part.P_SIZE,
                        container=part.P_CONTAINER, retailprice=part.P_RETAILPRICE,
                        comment=part.P_COMMENT)
    if form.validate_on_submit():
        part.P_PARTKEY = form.part_key.data
        part.P_NAME = form.name.data
        part.P_MFGR = form.MFGR.data
        part.P_BRAND = form.brand.data
        part.P_TYPE = form.type.data
        part.P_SIZE = form.size.data
        part.P_CONTAINER = form.container.data
        part.P_RETAILPRICE = form.retailprice.data
        part.P_COMMENT = form.comment.data

        db.session.commit()
        flash("????????????")
        return redirect(url_for('index'))
    else:
        return render_template('edit_part.html', form=form)


@app.route('/region', methods=['GET', 'POST'])
def region():
    form = SearchFormforRegion()
    if form.validate_on_submit():
        regions = Region.query.filter_by(R_REGIONKEY=form.regionkey.data).all()
    else:
        regions = Region.query.all()
    return render_template('region.html', title_name='??????', regions=regions, form=form)


@app.route('/add_region', methods=['GET', 'POST'])
def add_region():
    form = EditFormRegion()
    if form.validate_on_submit():
        try:
            region = Region(R_REGIONKEY=form.regionkey.data,
                            R_NAME=form.regionname.data, R_COMMENT=form.r_comment.data, PS_SUPPLYCOST=form.supplycost.data,
                            PS_COMMENT=form.ps_comment.data)
            db.session.add(region)
            db.session.commit()
            return redirect(url_for('region'))
        except Exception as e:
            print(e)
            flash("????????????")
            db.session.rollback()
            return render_template(u'edit_part.html', form=form)
    else:
        return render_template('edit_part.html', form=form)


@app.route('/edit_region/<int:id>', methods=['GET', 'POST'])
def edit_region(id):
    region = Region.query.get(id)
    form = EditFormRegion(regionkey=region.R_REGIONKEY, regionname=region.R_NAME,
                          r_comment=region.R_COMMENT, supplycost=region.PS_SUPPLYCOST,
                          ps_comment=region.PS_COMMENT)
    if form.validate_on_submit():
        region.R_REGIONKEY = form.regionkey.data
        region.R_NAME = form.regionname.data
        region.R_COMMENT = form.r_comment.data
        region.PS_SUPPLYCOST = form.supplycost.data
        region.PS_COMMENT = form.ps_comment.data

        db.session.commit()
        flash("????????????")
        return redirect(url_for('region'))
    else:
        return render_template('edit_part.html', form=form)


@app.route('/delete_region/<int:id>', methods=['GET', 'POST'])
def delete_region(id):
    region = Region.query.get(id)
    if region:
        try:
            db.session.delete(region)
            db.session.commit()
            flash("????????????")
        except Exception as e:
            print(e)
            flash("????????????")
            db.session.rollback()
    else:
        flash("???????????????")
    print(url_for('region'))
    return redirect(url_for('region'))


@app.route('/nation', methods=['GET', 'POST'])
def nation():
    form = SearchFormforNation()
    if form.validate_on_submit():
        nations = Nation.query.filter_by(N_NATIONKEY=form.nationkey.data).all()
    else:
        nations = Nation.query.all()
    return render_template('nation.html', title_name='??????', nations=nations, Region=Region, form=form)


@app.route('/add_nation', methods=['GET', 'POST'])
def add_nation():
    form = EditFormNation()
    choices = [(a.R_REGIONKEY, '(%d)'%a.R_REGIONKEY + a.R_NAME) for a in Region.query.all()]
    form.n_regionkey.choices += choices
    if form.validate_on_submit():
        try:
            nation = Nation(N_NATIONKEY=form.nationkey.data, N_NAME=form.nationname.data,
                            N_REGIONKEY=form.n_regionkey.data, N_COMMENT=form.comment.data)
            db.session.add(nation)
            db.session.commit()
            return redirect(url_for('nation'))
        except Exception as e:
            print(e)
            flash("????????????")
            db.session.rollback()
            return render_template('edit_part.html', form=form)
    else:
        return render_template('edit_part.html', form=form)


@app.route('/edit_nation/<int:id>', methods=['GET', 'POST'])
def edit_nation(id):
    nation = Nation.query.get(id)
    form = EditFormNation(nationkey=nation.N_NATIONKEY, nationname=nation.N_NAME,
                            n_regionkey=nation.N_REGIONKEY, comment=nation.N_COMMENT)
    if form.validate_on_submit():
        nation.N_NATIONKEY = form.nationkey.data
        nation.N_NAME = form.nationname.data
        nation.N_REGIONKEY = form.n_regionkey.data
        nation.N_COMMENT = form.comment.data

        db.session.commit()
        flash("????????????")
        return redirect(url_for('nation'))
    else:
        return render_template('edit_part.html', form=form)


@app.route('/delete_nation/<int:id>', methods=['GET', 'POST'])
def delete_nation(id):
    nation = Nation.query.get(id)
    if nation:
        try:
            db.session.delete(nation)
            db.session.commit()
            flash("????????????")
        except Exception as e:
            print(e)
            flash("????????????")
            db.session.rollback()
    else:
        flash("???????????????")
    print(url_for('nation'))
    return redirect(url_for('nation'))


@app.route('/customer', methods=['GET', 'POST'])
def customer():
    form = SearchFormforCustomer()
    UpdateFormCustomer()
    if form.validate_on_submit():
        customers = Customer.query.filter_by(C_CUSTKEY=form.c_custkey.data).all()
    else:
        customers = Customer.query.all()
    return render_template('customer.html', title_name='??????', customers=customers, Nation=Nation, form=form)


@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    form = EditFormCustomer()
    if form.validate_on_submit():
        try:
            customer = Customer(C_CUSTKEY=form.custkey.data, C_NAME=form.name.data,
                                C_ADDRESS=form.address.data, C_NATIONKEY=form.c_nationkey.data,
                                C_PHONE=form.phone.data, C_ACCTBAL=form.acctbal.data,
                                C_MKTSEGMENT=form.mktsegment.data, C_COMMENT=form.comment.data)
            for i in form.phone.data:
                if i>'9':
                    flash("??????????????????")
                    return render_template('edit_part.html', form=form)
                if i<'0':
                    flash("??????????????????")
                    return render_template('edit_part.html', form=form)
            if (len(form.phone.data) != 11):
                flash("????????????")
                return render_template('edit_part.html', form=form)
            db.session.add(customer)
            db.session.commit()
            return redirect(url_for('customer'))
        except Exception as e:
            print(e)
            flash("????????????")
            db.session.rollback()
            return render_template('edit_part.html', form=form)
    else:
        return render_template('edit_part.html', form=form)


@app.route('/edit_customer/<int:id>', methods=['GET', 'POST'])
def edit_customer(id):
    customer = Customer.query.get(id)
    form = EditFormCustomer(custkey=customer.C_CUSTKEY, name=customer.C_NAME, address=customer.C_ADDRESS,
                            c_nationkey=customer.C_NATIONKEY, phone=customer.C_PHONE, acctbal=customer.C_ACCTBAL,
                            mktsegment=customer.C_MKTSEGMENT, comment=customer.C_COMMENT)
    if form.validate_on_submit():
        customer.C_CUSTKEY = form.custkey.data
        customer.C_NAME = form.name.data
        customer.C_ADDRESS = form.address.data
        customer.C_NATIONKEY = form.c_nationkey.data
        customer.C_PHONE = form.phone.data
        customer.C_ACCTBAL = form.acctbal.data
        customer.C_MKTSEGMENT = form.mktsegment.data
        customer.C_COMMENT = form.comment.data
        for i in form.phone.data:
            if i > '9':
                flash("??????????????????")
                return render_template('edit_part.html', form=form)
            if i < '0':
                flash("??????????????????")
                return render_template('edit_part.html', form=form)
        if (len(form.phone.data) != 11):
            flash("????????????")
            return render_template('edit_part.html', form=form)

        db.session.commit()
        flash("????????????")
        return redirect(url_for('customer'))
    else:
        return render_template('edit_part.html', form=form)


@app.route('/delete_customer/<int:id>', methods=['GET', 'POST'])
def delete_customer(id):
    customer = Customer.query.get(id)
    if customer:
        try:
            db.session.delete(customer)
            db.session.commit()
            flash("????????????")
        except Exception as e:
            print(e)
            flash("????????????")
            db.session.rollback()
    else:
        flash("???????????????")
    print(url_for('customer'))
    return redirect(url_for('customer'))


@app.route('/supplier', methods=['GET', 'POST'])
def supplier():
    form = SearchFormforSupplier()
    UpdateFormSupplier()
    if form.validate_on_submit():
        suppliers = Supplier.query.filter_by(S_SUPPKEY=form.suppkey.data).all()
    else:
        suppliers = Supplier.query.all()
    return render_template('supplier.html', title_name='??????', suppliers=suppliers, Nation=Nation, form=form)


@app.route('/add_supplier', methods=['GET', 'POST'])
def add_supplier():
    form = EditFormSupplier()
    if form.validate_on_submit():
        try:
            supplier = Supplier(S_SUPPKEY=form.suppkey.data, S_NAME=form.name.data,
                                S_ADDRESS=form.address.data, S_NATIONKEY=form.nationkey.data,
                                S_PHONE=form.phone.data, S_ACCTBAL=form.acctbal.data,
                                S_COMMENT=form.comment.data)
            for i in form.phone.data:
                if i>'9':
                    flash("??????????????????")
                    return render_template('edit_part.html', form=form)
                if i<'0':
                    flash("??????????????????")
                    return render_template('edit_part.html', form=form)
            if (len(form.phone.data) != 11):
                flash("????????????")
                return render_template('edit_part.html', form=form)
            db.session.add(supplier)
            db.session.commit()
            return redirect(url_for('supplier'))
        except Exception as e:
            print(e)
            flash("????????????")
            db.session.rollback()
            return render_template('edit_part.html', form=form)
    else:
        return render_template('edit_part.html', form=form)


@app.route('/edit_supplier/<int:id>', methods=['GET', 'POST'])
def edit_supplier(id):
    supplier = Supplier.query.get(id)
    form = EditFormSupplier(suppkey=supplier.S_SUPPKEY, name=supplier.S_NAME, address=supplier.S_ADDRESS,
                            nationkey=supplier.S_NATIONKEY, phone=supplier.S_PHONE, acctbal=supplier.S_ACCTBAL,
                            comment=supplier.S_COMMENT)
    if form.validate_on_submit():
        supplier.S_SUPPKEY = form.suppkey.data
        supplier.S_NAME = form.name.data
        supplier.S_ADDRESS = form.address.data
        supplier.S_NATIONKEY = form.nationkey.data
        supplier.S_PHONE = form.phone.data
        supplier.S_ACCTBAL = form.acctbal.data
        supplier.S_COMMENT = form.comment.data
        for i in form.phone.data:
            if i > '9':
                flash("??????????????????")
                return render_template('edit_part.html', form=form)
            if i < '0':
                flash("??????????????????")
                return render_template('edit_part.html', form=form)
        if (len(form.phone.data) != 11):
            flash("????????????")
            return render_template('edit_part.html', form=form)

        db.session.commit()
        flash("????????????")
        return redirect(url_for('supplier'))
    else:
        return render_template('edit_part.html', form=form)


@app.route('/delete_supplier/<int:id>', methods=['GET', 'POST'])
def delete_supplier(id):
    supplier = Supplier.query.get(id)
    if supplier:
        try:
            db.session.delete(supplier)
            db.session.commit()
            flash("????????????")
        except Exception as e:
            print(e)
            flash("????????????")
            db.session.rollback()
    else:
        flash("??????????????????")
    print(url_for('supplier'))
    return redirect(url_for('supplier'))


@app.route('/partsupp', methods=['GET', 'POST'])
def partsupp():
    form = SearchFormforPartsupp()
    UpdateFormPartsupp()
    if form.validate_on_submit():
        partsupps = Partsupp.query.filter_by(PS_PARTKEY=form.partkey.data, PS_SUPPKEY=form.suppkey.data).all()
    else:
        partsupps = Partsupp.query.all()
    return render_template('partsupp.html', title_name='????????????', partsupps=partsupps,
                           Part=Part, Supplier=Supplier, form=form)


@app.route('/add_partsupp', methods=['GET', 'POST'])
def add_partsupp():
    form = EditFormPartsupp()
    if form.validate_on_submit():
        try:
            partsupp = Partsupp(PS_PARTKEY=form.partkey.data,PS_SUPPKEY=form.suppkey.data,
                                PS_AVAILQTY=form.availqty.data, PS_SUPPLYCOST=form.supplycost.data,
                                PS_COMMENT=form.comment.data)
            db.session.add(partsupp)
            db.session.commit()
            return redirect(url_for('partsupp'))
        except Exception as e:
            print(e)
            flash("????????????")
            db.session.rollback()
            return render_template(u'edit_part.html', form=form)
    else:
        return render_template('edit_part.html', form=form)


@app.route('/edit_partsupp/<int:id1>/<int:id2>', methods=['GET', 'POST'])
def edit_partsupp(id1, id2):
    partsupp = Partsupp.query.filter_by(PS_SUPPKEY=id2, PS_PARTKEY=id1).first()
    form = EditFormPartsupp(partkey=partsupp.PS_PARTKEY, suppkey=partsupp.PS_SUPPKEY, availqty=partsupp.PS_AVAILQTY,
                            supplycost=partsupp.PS_SUPPLYCOST, comment=partsupp.PS_COMMENT)
    if form.validate_on_submit():
        partsupp.PS_PARTKEY = form.partkey.data
        partsupp.PS_SUPPKEY = form.suppkey.data
        partsupp.PS_AVAILQTY = form.availqty.data
        partsupp.PS_SUPPLYCOST = form.supplycost.data
        partsupp.PS_COMMENT = form.comment.data

        db.session.commit()
        flash("????????????")
        return redirect(url_for('partsupp'))
    else:
        return render_template('edit_part.html', form=form)


@app.route('/delete_partsupp/<int:id1>/<int:id2>', methods=['GET', 'POST'])
def delete_partsupp(id1, id2):
    partsupp = Partsupp.query.filter_by(PS_SUPPKEY=id2, PS_PARTKEY=id1).first()
    if Partsupp:
        try:
            db.session.delete(partsupp)
            db.session.commit()
            flash("????????????")
        except Exception as e:
            print(e)
            flash("????????????")
            db.session.rollback()
    else:
        flash("?????????????????????")
    print(url_for('partsupp'))
    return redirect(url_for('partsupp'))


@app.route('/order', methods=['GET', 'POST'])
def order():
    form = SearchFormforOrders()
    UpdateFormOrders()
    if form.validate_on_submit():
        orders = Orders.query.filter_by(O_ORDERKEY=form.orderkey.data).all()
    else:
        orders = Orders.query.all()
    return render_template('order.html', title_name='??????', orders=orders, Customer=Customer, form=form)


@app.route('/add_order', methods=['GET', 'POST'])
def add_order():
    form = EditFormOrders()
    if form.validate_on_submit():
        try:
            order = Orders(O_ORDERKEY=form.orderkey.data, O_CUSTKEY=form.custkey.data, O_ORDERSTATUS=form.orderstatus.data,
                           O_TOTALPRICE=0, O_ORDERDATE=form.orderdate.data.strftime('%Y-%m-%d'), O_ORDERPRIORITY=form.orderpriority.data,
                           O_CLERK=form.clerk.data, O_SHIPPRIORITY=form.shippriority.data, O_COMMENT=form.comment.data)
            '''totals = Lineitem.query.filter_by(L_ORDERKEY=order.O_ORDERKEY).all()
            for i in totals:
                total = i.L_EXTENDEDPRICE
                order.O_TOTALPRICE += total'''
            db.session.add(order)
            db.session.commit()
            return redirect(url_for('order'))
        except Exception as e:
            print(e)
            flash("????????????")
            db.session.rollback()
            return render_template('edit_part.html', form=form)
    else:
        return render_template('edit_part.html', form=form)


@app.route('/delete_order/<int:id>', methods=['GET', 'POST'])
def delete_order(id):
    order = Orders.query.get(id)
    lineitems = Lineitem.query.filter_by(L_ORDERKEY=id).all()
    if order:
        try:
            for lineitem in lineitems:
                db.session.delete(lineitem)
            db.session.delete(order)
            db.session.commit()
            flash("????????????")
        except Exception as e:
            print(e)
            flash("????????????")
            db.session.rollback()
    else:
        flash("???????????????")
    print(url_for('order'))
    return redirect(url_for('order'))


@app.route('/edit_order/<int:id>', methods=['GET', 'POST'])
def edit_order(id):
    order = Orders.query.get(id)
    form = EditFormOrders(orderkey=order.O_ORDERKEY, custkey=order.O_CUSTKEY, orderstatus=order.O_ORDERSTATUS,
                        orderdate=order.O_ORDERDATE, orderpriority=order.O_ORDERPRIORITY, clerk=order.O_CLERK, shippriority=order.O_SHIPPRIORITY,
                        comment=order.O_COMMENT)
    if form.validate_on_submit():
        order.O_ORDERKEY = form.orderkey.data
        order.O_CUSTKEY = form.custkey.data
        order.O_ORDERSTATUS = form.orderstatus.data
        order.O_ORDERDATE = form.orderdate.data.strftime('%Y-%m-%d')
        order.O_ORDERPRIORITY = form.orderpriority.data
        order.O_CLERK = form.clerk.data
        order.O_SHIPPRIORITY = form.shippriority.data
        order.O_COMMENT = form.comment.data
        lineitems = Lineitem.query.filter_by(L_ORDERKEY=id).all()
        for lineitem in lineitems:
            lineitem.L_ORDERKEY = form.orderkey.data
        '''totals = Lineitem.query.filter_by(L_ORDERKEY=order.O_ORDERKEY).all()
        for i in totals:
            total = i.L_EXTENDEDPRICE
            order.O_TOTALPRICE += total'''

        db.session.commit()
        flash("????????????")
        return redirect(url_for('order'))
    else:
        return render_template('edit_part.html', form=form)


@app.route('/lineitem', methods=['GET', 'POST'])
def lineitem():
    form = SearchFormforLineitem()
    UpdateFormLineitem()
    if form.validate_on_submit():
        lineitems = Lineitem.query.filter_by(L_ORDERKEY=form.orderkey.data, L_LINENUMBER=form.linenumber.data).all()
    else:
        lineitems = Lineitem.query.all()
    return render_template('lineitem.html', title_name='????????????', lineitems=lineitems,
                           Part=Part, Supplier=Supplier, form=form)


@app.route('/add_lineitem', methods=['GET', 'POST'])
def add_lineitem():
    form = EditFormLineitem()
    if form.validate_on_submit():
        try:
            lineitem = Lineitem(L_ORDERKEY=form.orderkey.data, L_PARTKEY=form.partkey.data,
                                L_SUPPKEY=form.suppkey.data, L_LINENUMBER=form.linenumber.data,
                                L_QUANTITY=form.quantity.data,
                                L_EXTENDEDPRICE=form.quantity.data * Part.query.filter_by(P_PARTKEY=form.partkey.data).first().P_RETAILPRICE * form.discount.data,
                                L_DISCOUNT=form.discount.data, L_TAX=form.tax.data,
                                L_RETURNFLAG=form.returnflag.data, L_LINESTATUS=form.linestatus.data,
                                L_SHIPDATE=form.shipdate.data.strftime('%Y-%m-%d'), L_COMMITDATE=form.commitdate.data.strftime('%Y-%m-%d'),
                                L_RECEIPTDATE=form.receiptdate.data.strftime('%Y-%m-%d'), L_SHIPINSTRUCT=form.shipinstruct.data,
                                L_SHIPMODE=form.shipmode.data, L_COMMENT=form.comment.data)
            order = Orders.query.filter_by(O_ORDERKEY=form.orderkey.data).first()
            order.O_TOTALPRICE += lineitem.L_EXTENDEDPRICE

            db.session.add(lineitem)
            db.session.commit()
            return redirect(url_for('lineitem'))
        except Exception as e:
            print(e)
            flash("????????????")
            db.session.rollback()
            return render_template(u'edit_part.html', form=form)
    else:
        return render_template('edit_part.html', form=form)


@app.route('/edit_lineitem/<int:id1>/<int:id2>', methods=['GET', 'POST'])
def edit_lineitem(id1, id2):
    lineitem = Lineitem.query.filter_by(L_ORDERKEY=id1, L_LINENUMBER=id2).first()
    form = EditFormLineitem(orderkey=lineitem.L_ORDERKEY, partkey=lineitem.L_PARTKEY, suppkey=lineitem.L_SUPPKEY,
                            linenumber=lineitem.L_LINENUMBER, quantity=lineitem.L_QUANTITY,
                            discount=lineitem.L_DISCOUNT, tax=lineitem.L_TAX, returnflag=lineitem.L_RETURNFLAG,
                            linestatus=lineitem.L_LINESTATUS, shipdate=lineitem.L_SHIPDATE, commitdate=lineitem.L_COMMITDATE,
                            receiptdate=lineitem.L_RECEIPTDATE, shipinstruct=lineitem.L_SHIPINSTRUCT, shipmode=lineitem.L_SHIPMODE,
                            comment=lineitem.L_COMMENT)
    if form.validate_on_submit():
        if lineitem.L_ORDERKEY == form.orderkey.data:
            if lineitem.L_LINENUMBER == form.linenumber.data:
                '''order = Orders.query.filter_by(O_ORDERKEY=id1).first()
                order.O_TOTALPRICE -= lineitem.L_EXTENDEDPRICE'''
                lineitem.L_PARTKEY = form.partkey.data
                lineitem.L_SUPPKEY = form.suppkey.data
                lineitem.L_QUANTITY = form.quantity.data
                lineitem.L_EXTENDEDPRICE = form.quantity.data * Part.query.filter_by(
                    P_PARTKEY=form.partkey.data).first().P_RETAILPRICE * form.discount.data
                lineitem.L_DISCOUNT = form.discount.data
                lineitem.L_TAX = form.tax.data
                lineitem.L_RETURNFLAG = form.returnflag.data
                lineitem.L_LINESTATUS = form.linestatus.data
                lineitem.L_SHIPDATE = form.shipdate.data.strftime('%Y-%m-%d')
                lineitem.L_COMMITDATE = form.commitdate.data.strftime('%Y-%m-%d')
                lineitem.L_RECEIPTDATE = form.receiptdate.data.strftime('%Y-%m-%d')
                lineitem.L_SHIPINSTRUCT = form.shipinstruct.data
                lineitem.L_SHIPMODE = form.shipmode.data
                lineitem.L_COMMENT = form.comment.data
                '''order.O_TOTALPRICE += form.quantity.data * Part.query.filter_by(
                    P_PARTKEY=form.partkey.data).first().P_RETAILPRICE * form.discount.data'''
            else:
                lineitem.L_PARTKEY = form.partkey.data
                lineitem.L_SUPPKEY = form.suppkey.data
                lineitem.L_LINENUMBER = form.linenumber.data
                lineitem.L_QUANTITY = form.quantity.data
                lineitem.L_EXTENDEDPRICE = form.quantity.data * Part.query.filter_by(
                    P_PARTKEY=form.partkey.data).first().P_RETAILPRICE * form.discount.data
                lineitem.L_DISCOUNT = form.discount.data
                lineitem.L_TAX = form.tax.data
                lineitem.L_RETURNFLAG = form.returnflag.data
                lineitem.L_LINESTATUS = form.linestatus.data
                lineitem.L_SHIPDATE = form.shipdate.data.strftime('%Y-%m-%d')
                lineitem.L_COMMITDATE = form.commitdate.data.strftime('%Y-%m-%d')
                lineitem.L_RECEIPTDATE = form.receiptdate.data.strftime('%Y-%m-%d')
                lineitem.L_SHIPINSTRUCT = form.shipinstruct.data
                lineitem.L_SHIPMODE = form.shipmode.data
                lineitem.L_COMMENT = form.comment.data
                '''order.O_TOTALPRICE += form.quantity.data * Part.query.filter_by(
                    P_PARTKEY=form.partkey.data).first().P_RETAILPRICE * form.discount.data'''
        else:
            '''order = Orders.query.filter_by(O_ORDERKEY=id1).first()
            order.O_TOTALPRICE -= lineitem.L_EXTENDEDPRIC'''
            lineitem.L_ORDERKEY = form.orderkey.data
            lineitem.L_PARTKEY = form.partkey.data
            lineitem.L_SUPPKEY = form.suppkey.data
            lineitem.L_LINENUMBER = form.linenumber.data
            lineitem.L_QUANTITY = form.quantity.data
            lineitem.L_EXTENDEDPRICE = form.quantity.data * Part.query.filter_by(
                P_PARTKEY=form.partkey.data).first().P_RETAILPRICE * form.discount.data
            lineitem.L_DISCOUNT = form.discount.data
            lineitem.L_TAX = form.tax.data
            lineitem.L_RETURNFLAG = form.returnflag.data
            lineitem.L_LINESTATUS = form.linestatus.data
            lineitem.L_SHIPDATE = form.shipdate.data.strftime('%Y-%m-%d')
            lineitem.L_COMMITDATE = form.commitdate.data.strftime('%Y-%m-%d')
            lineitem.L_RECEIPTDATE = form.receiptdate.data.strftime('%Y-%m-%d')
            lineitem.L_SHIPINSTRUCT = form.shipinstruct.data
            lineitem.L_SHIPMODE = form.shipmode.data
            lineitem.L_COMMENT = form.comment.data
            '''order.O_TOTALPRICE += form.quantity.data * Part.query.filter_by(
                P_PARTKEY=form.partkey.data).first().P_RETAILPRICE * form.discount.data'''
        order = Orders.query.filter_by(O_ORDERKEY=id1).first()
        lineitems = Lineitem.query.filter_by(L_ORDERKEY=id1).all()
        order.O_TOTALPRICE = 0
        for line in lineitems:
            order.O_TOTALPRICE += line.L_QUANTITY * Part.query.filter_by(
                P_PARTKEY=form.partkey.data).first().P_RETAILPRICE * line.L_DISCOUNT

        db.session.commit()
        flash("????????????")
        return redirect(url_for('lineitem'))
    else:
        return render_template('edit_part.html', form=form)


@app.route('/delete_lineitem/<int:id1>/<int:id2>', methods=['GET', 'POST'])
def delete_lineitem(id1, id2):
    lineitem = Lineitem.query.filter_by(L_ORDERKEY=id1, L_LINENUMBER=id2).first()
    if Lineitem:
        try:
            Orders.query.filter_by(O_ORDERKEY=id1).first().O_TOTALPRICE -= lineitem.L_EXTENDEDPRICE
            db.session.delete(lineitem)
            db.session.commit()
            flash("????????????")
        except Exception as e:
            print(e)
            flash("????????????")
            db.session.rollback()
    else:
        flash("?????????????????????")
    print(url_for('lineitem'))
    return redirect(url_for('lineitem'))


if __name__ == '__main__':
    app.run()
