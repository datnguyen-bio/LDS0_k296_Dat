import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Using menu
st.title("Trung Tâm Tin Học")
menu = ["0.blank", "1. Lý thuyết", "2. Phân tích dữ liệu", "3. Sentiment Analysis", "4. Recommendation System"]
choice = st.sidebar.selectbox('Menu', menu)
if choice == '0.blank':    
    st.subheader("[Trang chủ](https://csc.edu.vn)")
    st.write("Giảng viên hướng dẫn: ThS. Khuất Thùy Phương")
    st.write("Học viên thực hiện: Nguyễn Thành Đạt")
    
elif choice == '1. Lý thuyết':    
    st.subheader("[Đồ án tốt nghiệp Data Science](https://csc.edu.vn/data-science-machine-learning/Do-An-Tot-Nghiep-Data-Science---Machine-Learning_229)")
    st.write("""### 1.1. Dữ liệu:
    2 file dữ liệu, bao gồm:
    - Dữ liệu cơ bản của các nơi lưu trú tại thành phố Nha Trang, tỉnh Khánh Hòa
    - Dữ liệu các Đánh giá (điểm) và Nhận xét của khách hàng về các nơi lưu trú đó""")
    st.write("""### 1.2. Phân tích dữ liệu:
    - Phân tích EDA dữ liệu trên cả 02 file
    - ...""")
    st.write("""### 1.3. Sentiment Analysis:
    - ...""")
    st.write("""### 1.4. Recommendation System:
    - ...""")

elif choice == '2. Phân tích dữ liệu':
    df_hotels = pd.read_csv('hotel_comments_4.csv')
    st.write('# Phân tích dữ liệu')

    # 2.1. làm sạch dữ liệu
    st.subheader("2.1. Quá trình làm sạch dữ liệu")
    st.write("""### Bổ sung thông tin cho nơi lưu trú
    - website offline (.mhtml), 713 điểm lưu trú tại Nha Trang, từ booking.com, ngày 1/8/2024
    - crawl offline bằng BeautifulSoup
    - lấy tên, khoảng cách đến bãi biển (beachfront), khoảng cách đến trung tâm thành phố (distance).""")
    st.image('beautifulsoup.png', use_column_width=True)
    
    st.write("""### Đối với file thông tin của nơi lưu trú, bao gồm các bước sau:
    - Tạo cột Hotel_Name mới trên hotel_profile.csv = cột Hotel Name chỉ lấy giá trị trong ngoặc đơn
    - match Hotel_Name với tên trong dữ liệu booking.com
    - 61 nơi lưu trú có thông tin beachfront, 54 có distance
    - drop dòng trùng Hotel_Name', 'Hotel Address'""")
    st.image('booking.png', use_column_width=True)

    st.write("""### Đối với file thông tin của comment, bao gồm các bước sau:
    - clean dữ liệu, xuất file csv
    - drop dòng mà không có Hotel_ID trong hotel_profiles.csv
    - drop dòng Body hoặc Title trống
    - drop dòng 'Hotel ID', 'Reviewer Name', 'Body' trùng nhau
    - tách Stay detail thành ngày, tháng, năm
    - dùng langid để xác định ngôn ngữ Body, drop dòng mà Body != "vi"
    - """)
    st.image('comments.png', use_column_width=True)

    # 2.2. Phân tích dữ liệu theo lựa chọn khách sạn
    st.subheader("2.2. Phân tích dữ liệu chung")
    # Display the data types
    st.write(df_hotels.dtypes)
    # Display the summary statistics
    st.subheader("Summary Statistics")
    st.write(df_hotels.describe())
    # Visualize the distribution of a numeric column
    st.subheader("Distribution of a Numeric Column")
    numeric_col = st.selectbox("Select a numeric column", df_hotels.select_dtypes(include='number').columns)
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.histplot(data=df_hotels, x=numeric_col, ax=ax)
    st.pyplot(fig)

    cols_to_keep = ['Hotel_Rank', 'Total_Score', 'Location', 'Cleanliness','Service','Facilities','Value_for_money','Comfort_and_room_quality','beachfront','distance']
    df_hotels2 = df_hotels[cols_to_keep]
    df_hotels2 = df_hotels2.apply(pd.to_numeric, errors='coerce')
    #df_hotels2 = df_hotels2.dropna(how='any')
    # Visualize the correlation matrix
    st.subheader("Correlation Matrix")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(df_hotels2.corr(), annot=True, cmap='YlOrRd', ax=ax)
    st.pyplot(fig)
    
    # Allow the user to explore individual columns
    st.subheader("Explore Individual Columns")
    selected_column = st.selectbox("Select a column", df_hotels.columns)
    st.write(df_hotels[selected_column].unique())
    st.write(df_hotels[selected_column].value_counts())
    
    
    # 2.3. Phân tích dữ liệu theo lựa chọn khách sạn
    st.subheader("2.3. Phân tích dữ liệu theo lựa chọn khách sạn")
    # Đọc dữ liệu khách sạn
    #df_hotels = df_hotels.drop_duplicates(subset='Hotel ID', keep='first')
    # Lấy 40 khách sạn
    random_hotels = df_hotels.sample(n=40, random_state=1)
    #print(random_hotels)

    st.session_state.random_hotels = random_hotels
    
    # Kiểm tra xem 'selected_hotel_id' đã có trong session_state hay chưa
    if 'selected_hotel_id' not in st.session_state:
        # Nếu chưa có, thiết lập giá trị mặc định là None hoặc ID khách sạn đầu tiên
        st.session_state.selected_hotel_id = None
    
    # Theo cách cho người dùng chọn khách sạn từ dropdown
    # Tạo một tuple cho mỗi khách sạn, trong đó phần tử đầu là tên và phần tử thứ hai là ID
    hotel_options = [(row['Hotel_Name'], row['Hotel_ID']) for index, row in st.session_state.random_hotels.iterrows()]
    st.session_state.random_hotels
    
    # # Tạo một dropdown với options là các tuple này
    selected_hotel = st.selectbox(
        "Chọn khách sạn",
        options=hotel_options,
        format_func=lambda x: x[0]  # Hiển thị tên khách sạn
    )
    # Display the selected hotel
    st.write("Bạn đã chọn:", selected_hotel)
    
    # Cập nhật session_state dựa trên lựa chọn hiện tại
    st.session_state.selected_hotel_id = selected_hotel[1]
    
    if st.session_state.selected_hotel_id:
        st.write("Hotel_ID: ", st.session_state.selected_hotel_id)
        # Hiển thị thông tin khách sạn được chọn
        selected_hotel = df_hotels[df_hotels['Hotel_ID'] == st.session_state.selected_hotel_id]

    # Display the selected hotel information
        st.write("### Bảng dữ liệu review thô, về điểm lưu trú đã chọn (chỉ bằng tiếng Việt):")
        st.dataframe(selected_hotel)
        st.write("#### Khoảng cách của điểm lưu trú đến bãi biển/trung tâm (theo booking.com)")
    
        # Get the distance of the hotel from the selected hotel beachfront
        distance_value = selected_hotel['beachfront'].values[0] if not selected_hotel.empty else None
        # Show the message based on distance value
        if pd.isna(distance_value):
            st.write("Không có thông tin về khoảng cách tới bãi biển.")
        else:
            st.write(f"Khoảng cách đến bãi biển là {distance_value} km.")
    
         # Get the distance of the hotel from the selected hotel distance
        distance_value2 = selected_hotel['distance'].values[0] if not selected_hotel.empty else None
        # Show the message based on distance value
        if pd.isna(distance_value2):
            st.write("Không có thông tin về khoảng cách tới trung tâm thành phố.")
        else:
            st.write(f"Khoảng cách đến trung tâm thành phố là {distance_value2} km.")

        #Các kết quả khác của điểm lưu trú
        # Total Score
        total_score = selected_hotel['Total_Score'].values[0] if not selected_hotel.empty else None
        # Show the message based on distance value
        if pd.isna(total_score):
            st.write("Không có thông tin về điểm tổng trung bình.")
        else:
            st.write(f"Điểm tổng trung bình là {total_score}.")

        # Location
        location = selected_hotel['Location'].values[0] if not selected_hotel.empty else None
        # Show the message based on distance value
        if pd.isna(location):
            st.write("Không có thông tin về điểm trung bình của vị trí.")
        else:
            st.write(f"Điểm vị trí trung bình là {location}.")

        # cleanliness
        cleanliness = selected_hotel['Cleanliness'].values[0] if not selected_hotel.empty else None
        # Show the message based on distance value
        if pd.isna(cleanliness):
            st.write("Không có thông tin về điểm trung bình của sự sạch sẽ.")
        else:
            st.write(f"Điểm sạch sẽ trung bình là {cleanliness}.")

        # service
        service = selected_hotel['Service'].values[0] if not selected_hotel.empty else None
        # Show the message based on distance value
        if pd.isna(service):
            st.write("Không có thông tin về điểm trung bình của dịch vụ.")
        else:
            st.write(f"Điểm dịch vụ trung bình là {service}.")

        # facilities
        facilities = selected_hotel['Facilities'].values[0] if not selected_hotel.empty else None
        # Show the message based on distance value
        if pd.isna(facilities):
            st.write("Không có thông tin về điểm trung bình của sự tiện nghi.")
        else:
            st.write(f"Điểm tiện nghi trung bình là {facilities}.")

        # value
        value = selected_hotel['Value_for_money'].values[0] if not selected_hotel.empty else None
        # Show the message based on distance value
        if pd.isna(value):
            st.write("Không có thông tin về điểm trung bình của sự đáng giá tiền.")
        else:
            st.write(f"Điểm đáng giá trung bình là {value}.")

        # comfortandquality
        comfortandquality = selected_hotel['Comfort_and_room_quality'].values[0] if not selected_hotel.empty else None
        # Show the message based on distance value
        if pd.isna(comfortandquality):
            st.write("Không có thông tin về điểm trung bình của sự thoải mái và chất lượng phòng.")
        else:
            st.write(f"Điểm thoải mái và chất lượng phòng trung bình là {comfortandquality}.")

        # Show basic statistics
        st.write("#### Thống kê mô tả về khách sạn")
        #st.write(selected_hotel.describe())
        numerical_cols = selected_hotel.select_dtypes(include='number')
        numerical_cols = numerical_cols.drop(columns=['num','distance', 'beachfront'], errors='ignore')
        st.write(numerical_cols.describe())
    
        # Calculate average score per stay_month
        st.write("#### Điểm số trung bình theo tháng")
        average_scores = selected_hotel.groupby('stay_month')['Score'].mean().reset_index()
        # Create a line chart
        plt.figure(figsize=(10, 6))
        plt.plot(average_scores['stay_month'], average_scores['Score'], marker='o')
        # Annotate average scores
        for i, row in average_scores.iterrows():
            plt.text(row['stay_month'], row['Score'] + 0.05, f"{row['Score']:.2f}", ha='center')
        # Set x-ticks from 1 to 12
        plt.xticks(range(1, 13))
        # Adjusting the y-axis to start from the minimum average score
        plt.ylim(bottom=min(average_scores['Score']) - 0.5)
        #plt.title('Average Score vs. Stay Month')
        plt.xlabel('Tháng')
        plt.ylabel('Điểm trung bình')
        st.pyplot(plt)
    
        # Show the count of ratings
        st.write("#### Phân phối điểm đánh giá")
        st.bar_chart(selected_hotel['Score'].value_counts())
    
        # Calculate average score by Room Type and Group Name
        st.write("#### Điểm trung bình theo loại phòng và nhóm khách hàng")
        # average_scores2 = selected_hotel.groupby(['Room Type', 'Group Name'])['Score'].mean().reset_index()
        # # # Display the average scores
        # # st.dataframe(average_scores2)
    
        # Calculate average score by Room Type and Group Name
        average_scores2 = (
            selected_hotel.groupby(['Room Type', 'Group Name'])['Score']
            .mean()
            .unstack()
        )
        # Create a heatmap
        plt.figure(figsize=(12, 8))
        sns.heatmap(average_scores2, annot=True, cmap='coolwarm', fmt='.2f', cbar_kws={'label': 'Average Score'})
        plt.xlabel('Nhóm khách hàng')
        plt.ylabel('Loại phòng')
        st.pyplot(plt)

        #wordcloud
        st.write("#### Wordcloud")
        text = selected_hotel['Processed_Body'].values[0] if not selected_hotel.empty else None
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        # Display the word cloud
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.set_axis_off()
        st.pyplot(fig)

elif choice == '3. Sentiment Analysis':
    df_hotels = pd.read_csv('hotel_comments_4.csv')
    st.subheader("3. Sentiment Analysis")

        # Load the trained models and the TF-IDF vectorizer
    with open('svm_model.pkl', 'rb') as f:
        svm_model = pickle.load(f)
    with open('random_forest_model.pkl', 'rb') as f:
        random_forest_model = pickle.load(f)
    with open('naive_bayes_model.pkl', 'rb') as f:
        naive_bayes_model = pickle.load(f)
    with open('logistic_regression_model.pkl', 'rb') as f:
        logistic_regression_model = pickle.load(f)
    with open('k-nn_model.pkl', 'rb') as f:
        knn_model = pickle.load(f)
    with open('decision_tree_model.pkl', 'rb') as f:
        decision_tree_model = pickle.load(f)
    with open('tfidf_vectorizer.pkl', 'rb') as f:
        tfidf_vectorizer = pickle.load(f)
    
    # Streamlit app
    st.title("Kiểm tra câu")
    
    # Allow the user to enter text
    user_input = st.text_area("Nhập đoạn review:")
    
    # Classify the user input using the trained models
    if st.button("Classify"):
        if user_input:
            # Vectorize the user input using the TF-IDF vectorizer
            X = tfidf_vectorizer.transform([user_input])
    
            # Make predictions using the trained models
            svm_prediction = svm_model.predict(X)[0]
            random_forest_prediction = random_forest_model.predict(X)[0]
            naive_bayes_prediction = naive_bayes_model.predict(X)[0]
            logistic_regression_prediction = logistic_regression_model.predict(X)[0]
            knn_prediction = knn_model.predict(X)[0]
            decision_tree_prediction = decision_tree_model.predict(X)[0]
    
            # Display the results
            st.write("Kết quả theo SVM:", svm_prediction)
            st.write("Kết quả theo Random Forest:", random_forest_prediction)
            st.write("Kết quả theo Naive Bayes:", naive_bayes_prediction)
            st.write("Kết quả theo Logistic Regression:", logistic_regression_prediction)
            st.write("Kết quả theo K-NN:", knn_prediction)
            st.write("Kết quả theo Decision Tree:", decision_tree_prediction)
        else:
            st.write("Hãy nhập đoạn review.")
    
elif choice == '4. Recommendation System':
    st.subheader("4. Recommendation System")
    # function cần thiết
    def get_recommendations(df, hotel_id, cosine_sim, nums=5):
        # Get the index of the hotel that matches the hotel_id
        matching_indices = df.index[df['Hotel_ID'] == hotel_id].tolist()
        if not matching_indices:
            print(f"No hotel found with ID: {hotel_id}")
            return pd.DataFrame()  # Return an empty DataFrame if no match
        idx = matching_indices[0]
    
        # Get the pairwise similarity scores of all hotels with that hotel
        sim_scores = list(enumerate(cosine_sim[idx]))
    
        # Sort the hotels based on the similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
        # Get the scores of the nums most similar hotels (Ignoring the hotel itself)
        sim_scores = sim_scores[1:nums+1]
    
        # Get the hotel indices
        hotel_indices = [i[0] for i in sim_scores]
    
        # Return the top n most similar hotels as a DataFrame
        return df.iloc[hotel_indices]
    
    # Hiển thị đề xuất ra bảng
    def display_recommended_hotels(recommended_hotels, cols=5):
        for i in range(0, len(recommended_hotels), cols):
            cols = st.columns(cols)
            for j, col in enumerate(cols):
                if i + j < len(recommended_hotels):
                    hotel = recommended_hotels.iloc[i + j]
                    with col:   
                        st.write(hotel['Hotel_Name'])                    
                        expander = st.expander(f"Description")
                        hotel_description = hotel['Hotel_Description']
                        truncated_description = ' '.join(hotel_description.split()[:100]) + '...'
                        expander.write(truncated_description)
                        expander.markdown("Nhấn vào mũi tên để đóng hộp text này.")           
    
    # Đọc dữ liệu khách sạn
    df_hotels = pd.read_csv('hotel_comments_4.csv')
    #df_hotels = df_hotels.drop_duplicates(subset='Hotel ID', keep='first')
    # Lấy 20 khách sạn
    random_hotels = df_hotels.sample(n=40, random_state=1)
    
    st.session_state.random_hotels = random_hotels
    
    # Open and read file to cosine_sim_new
    with open('cosine_sim.pkl', 'rb') as f:
        cosine_sim_new = pickle.load(f)
        
    st.image('hotel.jpeg', use_column_width=True)
    
    st.write('# Phân tích dữ liệu cơ bản + Recomendation System: khách sạn ở Nha Trang ')
    
    # Kiểm tra xem 'selected_hotel_id' đã có trong session_state hay chưa
    if 'selected_hotel_id' not in st.session_state:
        # Nếu chưa có, thiết lập giá trị mặc định là None hoặc ID khách sạn đầu tiên
        st.session_state.selected_hotel_id = None
    
    # Theo cách cho người dùng chọn khách sạn từ dropdown
    # Tạo một tuple cho mỗi khách sạn, trong đó phần tử đầu là tên và phần tử thứ hai là ID
    hotel_options = [(row['Hotel_Name'], row['Hotel_ID']) for index, row in st.session_state.random_hotels.iterrows()]
    st.session_state.random_hotels
    
    # # Tạo một dropdown với options là các tuple này
    selected_hotel = st.selectbox(
        "Chọn khách sạn",
        options=hotel_options,
        format_func=lambda x: x[0]  # Hiển thị tên khách sạn
    )
    # Display the selected hotel
    st.write("Bạn đã chọn:", selected_hotel)
    
    # Cập nhật session_state dựa trên lựa chọn hiện tại
    st.session_state.selected_hotel_id = selected_hotel[1]
    
    if st.session_state.selected_hotel_id:
        st.write("Hotel_ID: ", st.session_state.selected_hotel_id)
        # Hiển thị thông tin khách sạn được chọn
        selected_hotel = df_hotels[df_hotels['Hotel_ID'] == st.session_state.selected_hotel_id]
    
    
        if not selected_hotel.empty:
            st.write('#### Bạn vừa chọn:')
            st.write('### ', selected_hotel['Hotel_Name'].values[0])
    
            hotel_description = selected_hotel['Hotel_Description'].values[0]
            truncated_description = ' '.join(hotel_description.split()[:200])
            st.write('##### Thông tin:')
            st.write(truncated_description, '...')
    
            st.write('##### Các khách sạn khác bạn cũng có thể quan tâm:')
            recommendations = get_recommendations(df_hotels, st.session_state.selected_hotel_id, cosine_sim=cosine_sim_new, nums=4) 
            display_recommended_hotels(recommendations, cols=4)
        else:
            st.write(f"Không tìm thấy khách sạn với ID: {st.session_state.selected_hotel_id}")
