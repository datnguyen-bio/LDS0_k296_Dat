import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

# Using menu
st.title("Trung Tâm Tin Học")
menu = ["0a. Trang chủ trung tâm","0b. testing","0c. Nhập thông tin cá nhân (test streamlit)", "1. Lý thuyết", "2. Phân tích dữ liệu", "3. Sentiment Analysis", "4. Recommendation System"]
choice = st.sidebar.selectbox('Menu', menu)
if choice == 'Home':    
    st.subheader("[Trang chủ](https://csc.edu.vn)")  
elif choice == '0b. testing':    
    st.subheader("[Đồ án TN Data Science](https://csc.edu.vn/data-science-machine-learning/Do-An-Tot-Nghiep-Data-Science---Machine-Learning_229)")
    st.write("""### Có 2 chủ đề trong khóa học:
    - Topic 1: Sentiment Analysis
    - Topic 2: Recommendation System
    - ...""")
elif choice == '0. Nhập thông tin cá nhân (test streamlit)':
    # Sử dụng các điều khiển nhập
    # 1. Text
    st.subheader("1. Thông tin cá nhân")
    name = st.text_input("Nhập tên bạn")
    st.write("Bạn tên là: ", name)
    # 2. Slider
    st.subheader("2. Slider")
    age = st.slider("Tuổi của bạn?", 1, 100, 20)
    st.write("Bạn", age, "tuổi.")
    # 5. Selectbox
    st.subheader("5. Nghề nghiệp của bạn")
    occupation = st.selectbox("Bạn đang truy cập với vai trò?", ["Người học", "Giảng viên"])
    st.write("Bạn là ", occupation)
    # 6. Multiselect
    st.subheader("6. Địa điểm cư trú")
    location = st.multiselect("Bạn đang sống ở?", ("Hà Nội", "Thành phố Hồ Chí Minh", "Đà Nẵng", "Tỉnh thành khác"))
    st.write("Bạn đang sống ở", location)
   
    # Sử dụng điều khiển submit
    st.subheader("Submit")
    submitted = st.button("Submit")
    if submitted:
        st.write("You đã nhập thông tin.")
        # In các thông tin phía trên khi người dùng nhấn nút Submit
        st.write("Bạn tên là: ", name)
        st.write("Bạn", age, "tuổi.")
        st.write("Bạn là ", occupation)
        st.write("Bạn đang sống ở", location)

elif choice == '1. Lý thuyết':
    # 1.1. Line Chart
    st.subheader("1.1. Tổng quan lý thuyết")
    df = pd.DataFrame({
        'x': [1, 2, 3, 4, 5],
        'y': [10, 20, 30, 40, 50]
    })
    st.line_chart(df)
    # 2. Area Chart
    st.subheader("2. Area Chart")
    st.area_chart(df)
    # 3. Bar Chart
    st.subheader("3. Bar Chart")
    df = pd.DataFrame({
        'x': [1, 2, 3, 4, 5],
        'y': [10, 20, 30, 40, 50]
    })
    # vẽ biểu đồ bằng matplotlib
    fig, ax = plt.subplots()
    ax.bar(df['x'], df['y'])
    st.pyplot(fig)    
    # 4. Plot Map
    st.subheader("4. Plot Map")
    df = pd.DataFrame({
        'lat': [21.03, 21.02, 21.01],
        'lon': [105.85, 105.86, 105.85],
        'name': ['Hàng Trống', 'Phan Chu Trinh', 'Lê Đại Hành']
    })
    st.map(df)
    # 5. Plot Data
    # Dùng thư viện seaborn
    st.subheader("5. Plot Data")
    # Tạo dataframe
    data = {
        'x': [1, 2, 3, 4, 5],
        'y': [10, 20, 30, 40, 50]
    }
    df = pd.DataFrame(data)
    # Vẽ biểu đồ
    fig, ax = plt.subplots()
    sns.lineplot(data=df, x='x', y='y', ax=ax)
    st.pyplot(fig)
# Done

elif choice == '4. Recommendation System':
# function cần thiết
def get_recommendations(df, hotel_id, cosine_sim, nums=5):
    # Get the index of the hotel that matches the hotel_id
    matching_indices = df.index[df['Hotel ID'] == hotel_id].tolist()
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
# print(random_hotels)

# # Input for hotel ID
# random_hotels = st.text_input("Enter Hotel ID:")

# # Check if input is a valid integer and exists in the DataFrame
# if random_hotels.isdigit():
#     random_hotels = int(random_hotels)
#     if random_hotels in df_hotels['Hotel ID'].values:
#         st.write(f"Hotel ID {random_hotels} exists.")
#         selected_hotel = df_hotels[df_hotels['Hotel ID'] == random_hotels]
        
#         # Display the selected hotel information
#         st.write("Selected Hotel Information:")
#         st.dataframe(selected_hotel)
#     else:
#         st.write(f"Hotel ID {random_hotels} does not exist.")
# else:
#     st.write("Please enter a valid Hotel ID.")

st.session_state.random_hotels = random_hotels

# Open and read file to cosine_sim_new
with open('cosine_sim.pkl', 'rb') as f:
    cosine_sim_new = pickle.load(f)

###### Giao diện Streamlit ######
st.image('hotel.jpeg', use_column_width=True)

st.write('# Phân tích dữ liệu cơ bản + Recomendation System: khách sạn ở Nha Trang ')
st.write('#### Học viên: Nguyễn Thành Đạt')

# Kiểm tra xem 'selected_hotel_id' đã có trong session_state hay chưa
if 'selected_hotel_id' not in st.session_state:
    # Nếu chưa có, thiết lập giá trị mặc định là None hoặc ID khách sạn đầu tiên
    st.session_state.selected_hotel_id = None

# Theo cách cho người dùng chọn khách sạn từ dropdown
# Tạo một tuple cho mỗi khách sạn, trong đó phần tử đầu là tên và phần tử thứ hai là ID
hotel_options = [(row['Hotel_Name'], row['Hotel ID']) for index, row in st.session_state.random_hotels.iterrows()]
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
    st.write("Hotel ID: ", st.session_state.selected_hotel_id)
    # Hiển thị thông tin khách sạn được chọn
    selected_hotel = df_hotels[df_hotels['Hotel ID'] == st.session_state.selected_hotel_id]

    # Display the selected hotel information
    st.write("### Bảng dữ liệu review thô, về khách sạn (chỉ bằng tiếng Việt):")
    st.dataframe(selected_hotel)

    # Basic EDA
    st.write("#### Khoảng cách của khách sạn đến bãi biển/trung tâm (theo booking.com)")

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
        

    # # Encoding 'Group Name' into categorical codes
    # selected_hotel['Group Name Code'] = selected_hotel['Group Name'].astype('category').cat.codes
    # # Calculate the correlation matrix
    # correlation_matrix = selected_hotel[['Group Name Code', 'Score', 'stay_days_duration', 'stay_month']].corr()
    # # Display the correlation matrix
    # st.write("#### Correlation Matrix")
    # st.dataframe(correlation_matrix)
    # # Draw heatmap
    # plt.figure(figsize=(8, 6))
    # sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
    # plt.title('Correlation Heatmap')
    # st.pyplot(plt)

    
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

    # # Calculate average score and occurrence count by Room Type and Group Name
    # average_scores2 = (
    #     df_hotels.groupby(['Room Type', 'Group Name'])['Score']
    #     .agg(['mean', 'count'])
    #     .reset_index()
    # )
    
    # # Prepare the data for the heatmap
    # heatmap_data = average_scores2.pivot('Room Type', 'Group Name', 'mean')
    # occurrences_data = average_scores2.pivot('Room Type', 'Group Name', 'count')
    
    # # Create a heatmap
    # plt.figure(figsize=(12, 8))
    # sns.heatmap(heatmap_data, annot=occurrences_data, cmap='coolwarm', fmt='.2f',
    #             cbar_kws={'label': f'Average Score (n={selected_hotel.shape[0]})'}, linewidths=.5, linecolor='gray')
    # #plt.title('Average Score by Room Type and Group Name', fontsize=16)
    # plt.xlabel('Nhóm khách hàng', fontsize=12)
    # plt.ylabel('Loại phòng', fontsize=12)
    # plt.xticks(rotation=45, ha='right')
    # plt.yticks(rotation=0)

    # # Display the heatmap in Streamlit
    # #st.write("#### Heatmap of Average Score by Room Type and Group Name")
    # st.pyplot(plt)

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
