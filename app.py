
# This is basically the heart of my flask 

from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import pickle
import warnings
from time import sleep
warnings.filterwarnings("ignore")


app = Flask(__name__)
user_recommandation=pd.read_csv('dataset/user_final_rating_cos.csv')
user_recommandation.set_index('user',inplace=True)
# tfid = pickle.load(open('pickle/tfid.pkl','rb')) 
# randomforest = pickle.load(open('pickle/randomforest.pkl','rb'))
data=pd.read_csv('dataset/train.csv')

def html_code_table(prod_df,table_name,file_name,side):
    table_style = '<table border="1" style=" border: 2px solid; float: ' + side + '; width: 50%;">'
    table_head = '<caption style="text-align: left; caption-side: top; font-size: 140%; font-weight: bold; color:red;"><strong>' + table_name + '</strong></caption>'
    table_head_row = '<tr><th align= "left">Product Name</th><th align= "left">Positive %</th><th align= "left">Negative %</th></tr>'
    
    html_code = '<div align= "center">' + table_style + table_head + table_head_row
    
    for i in prod_df.index:
        row =  '<tr><td>' + str(prod_df['product'][i]) + '</td><td>' + str(prod_df['positive'][i]) +'</td><td>' + str(prod_df['negative'][i]) + '</td></tr>'
        html_code = html_code + row
        
    html_code = html_code + '</table>'+'</div>'
    
    file_path = 'templates/'
    
    hs = open(file_path + file_name + '.html', 'w')
    hs.write(html_code)


@app.route('/')
def home():
    return render_template('index.html',message="")



@app.route('/recommand', methods=['POST'])
def recommand():
    recommandation = pd.DataFrame(columns = ['product', 'positive','negative'])
    user=request.form['User'];
    if user in user_recommandation.index:
        sleep(5)
        result=user_recommandation.loc[user].sort_values(ascending=False)[0:20]
        prod=data[data['product'].isin(result.index)]
        final_recommandation=prod.sort_values('positive',ascending=False)[0:5]    
        res = True
        html_code_table(final_recommandation,'Products you may like','include','center')
        return render_template('index.html', recommended_product=res,user_name=user)

    else:
        return render_template('index.html', message="Invalid Input")


    


if __name__ == '__main__':
    app.run(debug=True)








