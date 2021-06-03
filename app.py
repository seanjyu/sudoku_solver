from flask import Flask,render_template,url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sudoku_solver import solver
app = Flask(__name__,template_folder='Template')
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200),nullable=False)
    date_created=db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' %self.id

@app.route('/',methods=['POST','GET'])
def index():
    if request.method =='POST':
        s=''
        for i in ["box_1","box_2","box_3","box_4","box_5","box_6","box_7","box_8","box_9","box_10","box_11","box_12","box_13","box_14","box_15","box_16","box_17","box_18","box_19","box_20","box_21","box_22","box_23","box_24","box_25","box_26","box_27","box_28","box_29","box_30","box_31","box_32","box_33","box_34","box_35","box_36","box_37","box_38","box_39","box_40","box_41","box_42","box_43","box_44","box_45","box_46","box_47","box_48","box_49","box_50","box_51","box_52","box_53","box_54","box_55","box_56","box_57","box_58","box_59","box_60","box_61","box_62","box_63","box_64","box_65","box_66","box_67","box_68","box_69","box_70","box_71","box_72","box_73","box_74","box_75","box_76","box_77","box_78","box_79","box_80","box_81"]:
            sudoku_square=request.form[i]
            if len(sudoku_square)==0:
                s+='0'
            else:  
                s+=sudoku_square
        if len(s)>81:
            return render_template('Error.html')
        sol=solver(s)
        
        if sol==False:
            return render_template('Error.html')
        else:
            return render_template('sol.html',sol=sol)
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)