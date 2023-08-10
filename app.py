from flask import Flask, render_template,request
import pickle
import numpy as np

app = Flask(__name__)

# Load 'popular.pkl'
with open('popularwp.pkl', 'rb') as file:
    popular_df = pickle.load(file)

with open('pt.pkl', 'rb') as file:
     pt= pickle.load(file)

with open('foods.pkl', 'rb') as file:
    foods = pickle.load(file)


with open('similarity_scores.pkl', 'rb') as file:
    similarity_scores = pickle.load(file)


@app.route('/')
def index():
    return render_template('index.html',
                           food_name=list(popular_df['name'].values),
                           price=list(popular_df['price'].values),
                           rating=list(popular_df['rating'].values))


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_foods', methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]

    data = []

    for i in similar_items:
        item = []
        temp_df = foods[foods['name'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('name')['name'].values))
        item.extend(list(temp_df.drop_duplicates('name')['price'].values))

        data.append(item)

    print(data)
    return render_template('recommend.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
