from flask import Flask,request,jsonify,render_template
import preprocessor,helper
import matplotlib.pyplot as plt
import matplotlib
import json
matplotlib.use('agg')



app = Flask(__name__)
@app.route('/',methods=['GET'])
def home():
     return render_template('home.html')

@app.route('/upload',methods=['POST'])
def upload_file():
    fileSrc = request.files['file']

    if fileSrc is not None:
        bytes_data = fileSrc.getvalue()
        data = bytes_data.decode("utf-8")
        df = preprocessor.preprocess(data)
        print('file converted to dataframe')

        # fetch unique users
        user_list = df['user'].unique().tolist()

        
        # user_list.remove('group_notification')
        user_list.sort()
        user_list.insert(0,"Overall")
        print('got user list')
        selected_user = user_list[0]
        print('got seleceted user')

        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)

        print("num_messages : ",num_messages)
        print("words : ",words)
        print("num_media_messages : ",num_media_messages)
        print("num_links : ",num_links)

        response = {'timeline':[],'daily_timeline':[],'busy_day':[],'busy_month':[],'x':[],'new_df':[],'word_cloud':[],'most_common_words':[],'emojis':[]}


        
        # monthly timeline
        timeline = helper.monthly_timeline(selected_user,df)      
        print("\nTimeline : ")
        print(timeline)

        timeline_dict = timeline.to_dict()
        response['timeline'] = timeline_dict
        
        # daily timeline
        daily_timeline = helper.daily_timeline(selected_user, df)
        daily_timeline_dict = daily_timeline.to_dict()
        response['daily_timeline'] = daily_timeline_dict

        busy_day = helper.week_activity_map(selected_user,df)
        response['busy_day'] = busy_day.to_dict()
   
        busy_month = helper.month_activity_map(selected_user, df)
        response['busy_month'] = busy_month.to_dict()
        
        

        # finding the busiest users in the group(Group level)
        if selected_user == 'Overall':

            x,new_df = helper.most_busy_users(df)
            response['x'] = x.to_dict()
            response['new_df'] = new_df.to_dict()
            
        # WordCloud
        df_wc = helper.create_wordcloud(selected_user,df)
        print(df_wc)
        print('\nWordCloud : ',df_wc)
        
        #most common words
        most_common_df = helper.most_common_words(selected_user,df)
        response['most_common_words'] = most_common_df.to_dict()
        
        #emoji analysis
        emoji_df = helper.analyze_emojis(selected_user,df)
        response['emojis'] = emoji_df.to_dict()
        # print('Emoji Analysis : ',emoji_df)
        
    responseJson = jsonify(response)
    return responseJson
    
if __name__ == '__main__':
    app.run(debug=True)