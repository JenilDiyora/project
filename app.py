from flask import Flask
from flask import render_template
app=Flask(__name__)

@app.route('/')
def hello_world():
   return {"msg":"ok"}

@app.route('/hello/<user>')
def rendertemplete(user):
       return render_template('hello.html',name=user)


@app.route('/mark/<int:score>')
def marktemplates(score):
       return render_template('mark.html',marks = score)

@app.route('/result')
def result():
       dect={'phy':50,'che':60,'maths':50}
       return render_template('dict.html',result=dect)
    
@app.route('/add')  
def add_data():
       
       
   return render_template('regi.html')

# @app.route('/view',methods = ['POST', 'GET'])
# def view_data(): 
   
#    # if request.method == 'POST':  
#    #    viewdata=request.form['fname']
#    #       return render_template('view.html',result=viewdata)
   
#    return render_template('view.html')

if __name__ == '__main__':
   app.run(debug=True)
   db.create_all()
   app.run()