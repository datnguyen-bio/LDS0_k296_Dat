import streamlit as st
import pandas as pd
import pickle
import matbplotlib as plt

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
random_hotels = df_hotels.sample(n=20, random_state=1)
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
        

    # Encoding 'Group Name' into categorical codes
    selected_hotel['Group Name Code'] = selected_hotel['Group Name'].astype('category').cat.codes
    # Calculate the correlation matrix
    correlation_matrix = selected_hotel[['Group Name Code', 'Score', 'stay_days_duration', 'stay_month']].corr()
    # Display the correlation matrix
    st.write("#### Correlation Matrix")
    st.dataframe(correlation_matrix)
    # Draw heatmap
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Correlation Heatmap')
    st.pyplot(plt)
    

    # Show basic statistics
    st.write("#### Thống kê mô tả về khách sạn")
    #st.write(selected_hotel.describe())
    numerical_cols = selected_hotel.select_dtypes(include='number')
    numerical_cols = numerical_cols.drop(columns=['num','distance', 'beachfront'], errors='ignore')
    st.write(numerical_cols.describe())

    # Show the count of ratings
    st.write("#### Phân phối điểm đánh giá")
    st.bar_chart(selected_hotel['Score'].value_counts())

    if not selected_hotel.empty:
        st.write('#### Bạn vừa chọn:')
        st.write('### ', selected_hotel['Hotel_Name'].values[0])

        hotel_description = selected_hotel['Hotel_Description'].values[0]
        truncated_description = ' '.join(hotel_description.split()[:100])
        st.write('##### Thông tin:')
        st.write(truncated_description, '...')

        st.write('##### Các khách sạn khác bạn cũng có thể quan tâm:')
        recommendations = get_recommendations(df_hotels, st.session_state.selected_hotel_id, cosine_sim=cosine_sim_new, nums=3) 
        display_recommended_hotels(recommendations, cols=3)
    else:
        st.write(f"Không tìm thấy khách sạn với ID: {st.session_state.selected_hotel_id}")
