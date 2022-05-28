from flask import Flask, render_template,url_for,flash,redirect
from forms import Registration_Form,Login_Form
app = Flask(__name__,static_url_path='/static')

app.config['SECRET_KEY'] = '91ccbe50f8623969238cc96e711fb88f' # secret key for form submittion , xss protection, cookie hacking


post_datas = [
    {
        'Author': 'Narotsit Karki',
        'Title': 'Great News for IT Student',
        'Content': 'NEW IT training center on the town',
        'Date': 'May 26 , 2022',
        'Comments': [
            {
                'User': 'Unkown',
                'Comment': 'Great Initiative',
                'Date': 'May 26, 2022'
            },
            {
                'User': 'Navraj@34',
                'Comment': 'Let us see what happens',
                'Date': 'May 29, 2022'
            },
            {
                'User':'Bhuvray',
                'Comment': 'What a bad idea 😂 😂',
                'Date': 'June 1, 2022'
            },
        ]
    },

    {
        'Author': 'Nabin Karki',
        'Title': 'Sniff Email with Scapy',
        'Content': 'Powerfull python module to sniff email and do others lot of network related things',
        'Date': 'May 20 , 2022',

        'Comments': [
            {
                'User': 'Chetan',
                'Comment': 'Great Presentation Loved it 🧡 🧡',
                'Date': 'May 21, 2022'
            },
            {
                'User': 'Naruto@12',
                'Comment': 'Please Bring more of these contents !!',
                'Date': 'May 22, 2022'
            },
            {
                'User':'Angel12',
                'Comment': 'What a exellent content 😍',
                'Date': 'May 25, 2022'
            },
        ]
    },
    {
        'Author': 'Subrat Regmi',
        'Title': 'Constraint Satisfaction problem',
        'Content': '(CSP) Constraint Satisfaction Problem of the Artificial Intelligence',
        'Date': 'June 21 , 2022',
'Comments': [
            {
                'User': 'Unknown',
                'Comment': 'Needed it very much Thanks 🧡💚💙💜💛',
                'Date': 'June 22, 2022'
            },
            {
                'User': 'GyanMust',
                'Comment': 'Please Bring more of these contents !!',
                'Date': 'June 21, 2022'
            },
            {
                'User':'Gorgeou1233',
                'Comment': 'Nicely Explained Loved it 💖',
                'Date': 'June 24, 2022'
            },
        ]
    }
]
@app.route('/')
def home():
    return render_template('index.html', tiltle ='Home')

@app.route('/posts')
def posts():
    return render_template('posts.html', title = 'Posts' , post_datas = post_datas)


@app.route('/about-us')
def about_us():
    return render_template('about-us.html', title = 'About-Us')


@app.route('/Login', methods = ['GET','POST'])
def login():
    form = Login_Form()
    return render_template('login.html',form  = form,title = 'Login')

@app.route('/Register', methods = ['GET','POST'])
def register():
    form = Registration_Form()
    if form.validate_on_submit():
        flash(f'Account Succesfully Created for {form.username.data}', 'successs')
        return redirect(url_for('home'))

    return render_template('register.html',form = form, title = 'Register')


if __name__ == '__main__':
    app.run(debug=True,host='192.168.137.162',port= 8000)
