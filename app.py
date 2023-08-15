from flask import Flask, render_template,request,jsonify, redirect, url_for,make_response
import pymysql
from flask_bcrypt import Bcrypt

app = Flask(__name__)

@app.route('/')
def index():
    alert = request.args.get('alert', '') 
    login_id=request.cookies.get('id')
    login_nickname=request.cookies.get('nickname')
    login_num=request.cookies.get('num')
    db_all_rating = pymysql.connect(host='localhost', user='root',
            password='1234', database='myweb3',
            autocommit=True, cursorclass=pymysql.cursors.DictCursor)
    with db_all_rating:
        db_cursor = db_all_rating.cursor()
        db_cursor.execute("SELECT * FROM rating")
        all_rating = db_cursor.fetchall()

        db_cursor.execute("select * from rating where movie_or_drama='movie';")
        movies = db_cursor.fetchall()

        db_cursor.execute("select * from rating where movie_or_drama='drama';")
        dramas = db_cursor.fetchall()

        db_cursor.execute("select img.poster_image from rating rt join image img on rt.id=img.id where rt.movie_or_drama='movie';")
        movie_poster_img = db_cursor.fetchall()

        db_cursor.execute("select img.poster_image from rating rt join image img on rt.id=img.id where rt.movie_or_drama='drama';")
        drama_poster_img = db_cursor.fetchall()

        db_cursor.execute("select * from video order by date desc;")
        recent_issues = db_cursor.fetchall()

        db_cursor.execute("select * from video;")
        videos = db_cursor.fetchall()

        db_cursor.execute("select sr.movie_id, count(movie_id),rt.name from search sr join rating rt on sr.movie_id=rt.id group by movie_id order by count(movie_id) desc limit 10;")
        searchranking= db_cursor.fetchall()

    return render_template('index.html', all=all_rating, movies=movies,dramas=dramas, movie_poster_img=movie_poster_img,
                           drama_poster_img=drama_poster_img, recent_issues=recent_issues, videos=videos,alert=alert,login_id=login_id,login_nickname=login_nickname,login_num=login_num,
                          searchranking=searchranking
                          )


@app.route('/movies.html')
def movies():
    login_id=request.cookies.get('id')
    login_nickname=request.cookies.get('nickname')
    login_num=request.cookies.get('num')

    db_all_rating = pymysql.connect(host='localhost', user='root',
            password='1234', database='myweb3',
            autocommit=True, cursorclass=pymysql.cursors.DictCursor)
    with db_all_rating:
        db_cursor = db_all_rating.cursor()
    
        db_cursor.execute("SELECT * FROM rating;")
        all_rating = db_cursor.fetchall()

        db_cursor.execute("select * from rating where movie_or_drama='movie';")
        movies = db_cursor.fetchall()

        db_cursor.execute("select img.poster_image from rating rt join image img on rt.id=img.id where rt.movie_or_drama='movie';")
        movie_poster_img = db_cursor.fetchall()
      
    return render_template('movies.html', all=all_rating,movies=movies,movie_poster_img=movie_poster_img,login_id=login_id,login_nickname=login_nickname,login_num=login_num,)



@app.route('/movies.html/modal', methods=['POST'])
def modal2():
    data=request.get_json()['data']

    data1="SELECT rt.name, rt.rating,date_format(rt.date,'%M %D, %Y') as date, img.poster_image,img.background_image,vd.video_title,vd.video_link FROM rating rt join image img on rt.id=img.id join video vd on img.id=vd.id where name='"+data+"';"
    

    db_all_rating = pymysql.connect(host='localhost', user='root',
            password='1234', database='myweb3',
            autocommit=True, cursorclass=pymysql.cursors.DictCursor)

    with db_all_rating:
        db_cursor = db_all_rating.cursor()
        db_cursor.execute(data1)
        all_rating = db_cursor.fetchall()

        db_cursor.execute("select id from rating where name ='"+data+"';")
        movie_id = db_cursor.fetchall()[0]['id']

        db_cursor.execute("select us.nickname, rv.comment from review rv join users us on rv.user_num=us.num where rv.movie_id='"+str(movie_id)+"' order by rv.id desc limit 5;")
        review = db_cursor.fetchall()

        
      
    return jsonify({'all_rating':all_rating,'review':review})


@app.route('/movies.html/sort', methods=['POST'])
def movie_sort():
    sort = request.form['sort']
    login_id=request.cookies.get('id')
    login_nickname=request.cookies.get('nickname')
    login_num=request.cookies.get('num')
    db_all_rating = pymysql.connect(host='localhost', user='root',
            password='1234', database='myweb3',
            autocommit=True, cursorclass=pymysql.cursors.DictCursor)
    db_cursor = db_all_rating.cursor()
    db_cursor.execute("SELECT * FROM rating;")
    all_rating = db_cursor.fetchall()

    if sort=='date':#날짜순으로 정렬
       db_cursor.execute("select * from rating where movie_or_drama='movie'order by date desc;")
       movies = db_cursor.fetchall()
       db_cursor.execute("select img.poster_image from rating rt join image img on rt.id=img.id where rt.movie_or_drama='movie'order by date desc;")
       movie_poster_img = db_cursor.fetchall()

    elif sort=='name':#이름순으로 정렬
       db_cursor.execute("select * from rating where movie_or_drama='movie'order by name asc;")
       movies = db_cursor.fetchall()
       db_cursor.execute("select img.poster_image from rating rt join image img on rt.id=img.id where rt.movie_or_drama='movie'order by name asc;")
       movie_poster_img = db_cursor.fetchall()

    else: #평점순으로 정렬
       db_cursor.execute("select * from rating where movie_or_drama='movie'order by rating desc;")
       movies = db_cursor.fetchall()
       db_cursor.execute("select img.poster_image from rating rt join image img on rt.id=img.id where rt.movie_or_drama='movie'order by rating desc;")
       movie_poster_img = db_cursor.fetchall()
    
    return render_template('movies.html', all=all_rating,movies=movies,movie_poster_img=movie_poster_img,login_id=login_id,login_nickname=login_nickname,login_num=login_num,)

@app.route('/tvshows.html')
def tvshows():
    login_id=request.cookies.get('id')
    login_nickname=request.cookies.get('nickname')
    login_num=request.cookies.get('num')
    db_all_rating = pymysql.connect(host='localhost', user='root',
            password='1234', database='myweb3',
            autocommit=True, cursorclass=pymysql.cursors.DictCursor)
    with db_all_rating:
        db_cursor = db_all_rating.cursor()
        db_cursor.execute("SELECT * FROM rating")
        all_rating = db_cursor.fetchall()

        db_cursor.execute("select * from rating where movie_or_drama='drama';")
        dramas = db_cursor.fetchall()

        db_cursor.execute("select img.poster_image from rating rt join image img on rt.id=img.id where rt.movie_or_drama='drama';")
        drama_poster_img = db_cursor.fetchall()
    return render_template('tvshows.html', all=all_rating,dramas=dramas,drama_poster_img=drama_poster_img,login_id=login_id,login_nickname=login_nickname,login_num=login_num,)

@app.route('/tvshows.html/modal', methods=['POST'])
def modal_tvshow():
    data=request.get_json()['data']
   
    data1="SELECT rt.name, rt.rating,date_format(rt.date,'%M %D, %Y') as date, img.poster_image,img.background_image,vd.video_title,vd.video_link FROM rating rt join image img on rt.id=img.id join video vd on img.id=vd.id where name='"+data+"';"
    
    db_all_rating = pymysql.connect(host='localhost', user='root',
            password='1234', database='myweb3',
            autocommit=True, cursorclass=pymysql.cursors.DictCursor)
    with db_all_rating:
        db_cursor = db_all_rating.cursor()
        db_cursor.execute(data1)
        all_rating = db_cursor.fetchall()

        db_cursor.execute("select id from rating where name ='"+data+"';")
        movie_id = db_cursor.fetchall()[0]['id']
        print(movie_id)
       

        db_cursor.execute("select us.nickname, rv.comment from review rv join users us on rv.user_num=us.num where rv.movie_id='"+str(movie_id)+"' order by rv.id desc limit 5;")
        review = db_cursor.fetchall()
        print(review)

        
      
    return jsonify({'all_rating':all_rating,'review':review})
      

@app.route('/tvshows.html/sort', methods=['POST'])
def drama_sort():
    sort = request.form['sort']
    print(sort)
    login_id=request.cookies.get('id')
    login_nickname=request.cookies.get('nickname')
    login_num=request.cookies.get('num')
    db_all_rating = pymysql.connect(host='localhost', user='root',
            password='1234', database='myweb3',
            autocommit=True, cursorclass=pymysql.cursors.DictCursor)
    db_cursor = db_all_rating.cursor()
    db_cursor.execute("SELECT * FROM rating;")
    all_rating = db_cursor.fetchall()

    if sort=='date':#날짜순으로 정렬
       db_cursor.execute("select * from rating where movie_or_drama='drama'order by date desc;")
       dramas = db_cursor.fetchall()
       db_cursor.execute("select img.poster_image from rating rt join image img on rt.id=img.id where rt.movie_or_drama='drama'order by date desc;")
       drama_poster_img = db_cursor.fetchall()

    elif sort=='name':#이름순으로 정렬
       db_cursor.execute("select * from rating where movie_or_drama='drama'order by name asc;")
       dramas = db_cursor.fetchall()
       db_cursor.execute("select img.poster_image from rating rt join image img on rt.id=img.id where rt.movie_or_drama='drama'order by name asc;")
       drama_poster_img = db_cursor.fetchall()
    
    else: #평점순으로 정렬
       db_cursor.execute("select * from rating where movie_or_drama='drama'order by rating desc;")
       dramas = db_cursor.fetchall()
       db_cursor.execute("select img.poster_image from rating rt join image img on rt.id=img.id where rt.movie_or_drama='drama'order by rating desc;")
       drama_poster_img = db_cursor.fetchall()
    
    #return redirect(url_for('tvshows',all=all_rating, dramas=dramas, drama_poster_img=drama_poster_img))
    return render_template('tvshows.html', all=all_rating, dramas=dramas, drama_poster_img=drama_poster_img,login_id=login_id,login_nickname=login_nickname,login_num=login_num,)

@app.route('/videos.html')
def videos():
    login_id=request.cookies.get('id')
    login_nickname=request.cookies.get('nickname')
    login_num=request.cookies.get('num')

    db_all_rating = pymysql.connect(host='localhost', user='root',
            password='1234', database='myweb3',
            autocommit=True, cursorclass=pymysql.cursors.DictCursor)
    db_cursor = db_all_rating.cursor()

    with db_all_rating:
        db_cursor.execute("select * from video;")
        videos = db_cursor.fetchall()

        db_cursor.execute("SELECT * FROM rating")
        all_rating = db_cursor.fetchall()
    return render_template('videos.html',all=all_rating, videos=videos,login_id=login_id,login_nickname=login_nickname,login_num=login_num,)

@app.route('/videos.html/modal', methods=['POST'])
def modal_videos():
    data=request.get_json()['data']
   
    data1="SELECT rt.name, rt.rating,date_format(rt.date,'%M %D, %Y') as date, img.poster_image,img.background_image,vd.video_title,vd.video_link FROM rating rt join image img on rt.id=img.id join video vd on img.id=vd.id where name='"+data+"';"
    
    db_all_rating = pymysql.connect(host='localhost', user='root',
            password='1234', database='myweb3',
            autocommit=True, cursorclass=pymysql.cursors.DictCursor)
    with db_all_rating:
        db_cursor = db_all_rating.cursor()
        db_cursor.execute(data1)
        all_rating = db_cursor.fetchall()

        db_cursor.execute("select id from rating where name ='"+data+"';")
        movie_id = db_cursor.fetchall()[0]['id']

        db_cursor.execute("select us.nickname, rv.comment from review rv join users us on rv.user_num=us.num where rv.movie_id='"+str(movie_id)+"' order by rv.id desc limit 5;")
        review = db_cursor.fetchall()
      
    return jsonify({'all_rating':all_rating,'review':review})

@app.route('/videos.html/sort', methods=['POST'])
def video_sort():
    sort = request.form['sort']
    login_id=request.cookies.get('id')
    login_nickname=request.cookies.get('nickname')
    login_num=request.cookies.get('num')
    db_all_rating = pymysql.connect(host='localhost', user='root',
            password='1234', database='myweb3',
            autocommit=True, cursorclass=pymysql.cursors.DictCursor)
    db_cursor = db_all_rating.cursor()
    db_cursor.execute("SELECT * FROM rating;")
    all_rating = db_cursor.fetchall()

    if sort=='date':#날짜순으로 정렬
       db_cursor.execute("select * from video order by date desc;")
       videos = db_cursor.fetchall()

    elif sort=='name':#이름순으로 정렬
       db_cursor.execute("select * from video order by video_title asc;")
       videos = db_cursor.fetchall()

    else: #평점순으로 정렬
       db_cursor.execute("select * from video vd join rating rt on vd.id=rt.id order by rt.rating desc;")
       videos = db_cursor.fetchall()
    #return redirect(url_for('videos',all=all_rating,videos=videos))
    return render_template('videos.html', all=all_rating,videos=videos,login_id=login_id,login_nickname=login_nickname,login_num=login_num,)

@app.route('/login.html')
def login():
    alert = request.args.get('alert', '') 
    return render_template('login.html',alert=alert)

@app.route('/login.html/login', methods=['POST'])
def login1():
    id = request.form.get('id')
    password = request.form.get('password')

    data="select * from users where id='"+id+"' and password='"+password+"';"
    print(data)
    db_all_rating = pymysql.connect(host='localhost', user='root',
            password='1234', database='myweb3',
            autocommit=True, cursorclass=pymysql.cursors.DictCursor)
    db_cursor = db_all_rating.cursor()
    db_cursor.execute(data)
    user_info = db_cursor.fetchall()
    if len(user_info)<=0:
         alert="아이디나 비밀번호가 존재하지 않습니다."
         return render_template('login.html',alert=alert)
    else:
        num=user_info[0]['num']
        nickname=user_info[0]['nickname']
        alert="로그인 완료"
        resp=make_response(redirect(url_for('index',alert=alert)) )
        resp.set_cookie('id',id)
        resp.set_cookie('password',password)
        resp.set_cookie('num',str(num))
        resp.set_cookie('nickname',nickname)
        return resp   

@app.route('/signup.html')
def signup():
  
    return render_template('signup.html')



@app.route('/signup.html/signup', methods=['POST'])
def signup1():
    id = request.form.get('id')
    password = request.form.get('password')
    nickname = request.form.get('nickname')
    data="select count(id) from users where id='"+id+"' ""or nickname='"+nickname+"';"
    
    db_all_rating = pymysql.connect(host='localhost', user='root',
                password='1234', database='myweb3',
                autocommit=True, cursorclass=pymysql.cursors.DictCursor)
    db_cursor = db_all_rating.cursor()
    db_cursor.execute(data)
    count = db_cursor.fetchall()

    if count[0]['count(id)']>0:
        alert="아이디나 닉네임이 이미 사용 중입니다."
        return render_template('signup.html',alert=alert)
    else:
        data="insert into users (id,password,nickname) values ('"+id+"', '"+password+"', '"+nickname+"');"
      
        db_cursor = db_all_rating.cursor()
        db_cursor.execute(data)
        alert="회원가입 완료! 로그인 해주세요."
        return redirect(url_for('login',alert=alert))
    
@app.route('/search', methods=['POST'])
def search():
    data=request.get_json()['data']

    db_all_rating = pymysql.connect(host='localhost', user='root',
            password='1234', database='myweb3',
            autocommit=True, cursorclass=pymysql.cursors.DictCursor)

    with db_all_rating:
        db_cursor = db_all_rating.cursor()
        db_cursor.execute("select id from rating where name ='"+data+"';")
        movie_id = db_cursor.fetchall()[0]['id']
        login_num=request.cookies.get('num')
        if login_num!=None:
            data1="insert into search (movie_id,user_num) values ('"+str(movie_id)+"', '"+str(login_num)+"');"
            db_cursor.execute(data1)
       
    return jsonify(success=True)
@app.route('/write', methods=['POST'])
def write():
    data = request.get_json()
    review = data['review']
    movie_name = data['movie_name']
    login_num=request.cookies.get('num')

    db_all_rating = pymysql.connect(host='localhost', user='root',
            password='1234', database='myweb3',
            autocommit=True, cursorclass=pymysql.cursors.DictCursor)
    db_cursor = db_all_rating.cursor()
    db_cursor.execute("select * from rating where name='"+movie_name+"';")
    movie_id=db_cursor.fetchall()[0]['id']
    db_cursor.execute("insert into review (user_num,movie_id,comment) values ('"+login_num+"', '"+str(movie_id)+"', '"+str(review)+"');")
    
    db_cursor.execute("select us.nickname, rv.comment from review rv join users us on rv.user_num=us.num where rv.movie_id='"+str(movie_id)+"' order by rv.id desc limit 5;")
    review = db_cursor.fetchall()
    
    return jsonify({'review':review})
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5001)
