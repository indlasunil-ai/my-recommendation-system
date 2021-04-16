
# This is basically the heart of my flask 

from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import pickle
import warnings
warnings.filterwarnings("ignore")


app = Flask(__name__)
user_recommandation=pd.read_csv('dataset/user_final_rating_cos.csv')
user_recommandation.set_index('user',inplace=True)
tfid = pickle.load(open('pickle/tfid.pkl','rb'))
randomforest = pickle.load(open('pickle/randomforest.pkl','rb'))
data=pd.read_csv('dataset/sample30_processed.csv')

def html_code_table(prod_df,table_name,file_name,side):
    table_style = '<table style="border: 2px solid; float: ' + side + '; width: 40%;">'
    table_head = '<caption style="text-align: left; caption-side: top; font-size: 140%; font-weight: bold; color:red;"><strong>' + table_name + '</strong></caption>'
    table_head_row = '<tr><th align= "left">Product Name</th></tr>'
    
    html_code = '<div align= "center">' + table_style + table_head + table_head_row
    
    for i in prod_df:
        row = '<tr><td>' + str(i) + '</td></tr>'
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
        result=user_recommandation.loc[user].sort_values(ascending=False)[0:20]
        prod=data[data['name'].isin(result.index)][['name','processed_text']]
        for product in prod['name'].unique():
            df=prod[prod['name']==product][['name','processed_text']]
            x_test=df['processed_text']
            X_TFID=tfid.transform(x_test).toarray()
            prob=randomforest.predict_proba(X_TFID)
            recommandation=recommandation.append({'product' : product, 'positive' : prob[:,1].sum(), 'negative' : prob[:,0].sum()}, 
                      ignore_index = True)

         
        print(recommandation)

        final_recommandation=recommandation[recommandation.positive > recommandation.negative].sort_values('positive',ascending=False)[0:5]
  
        
        res = True
        html_code_table(final_recommandation['product'],'Products you may like','include','center')
        return render_template('index.html', recommended_product=res,user_name=user)

    else:
        return render_template('index.html', message="Invalid Input")


    


if __name__ == '__main__':
    app.run(debug=True)








