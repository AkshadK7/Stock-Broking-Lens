import streamlit as st
from PIL import Image
import requests
import io
import base64
import json
import pandas as pd
from urllib.parse import quote 

BASE_URL = "http://localhost:8000"

# Streamlit Image Capture Frontend

st.title("Stock Broking Lens")
st.write("An AI-powered Visual Search Application to all the curious financial minds to tap and look into the current valuation of the object brands around you.")

#file_image = st.sidebar.file_uploader("Upload your Photos", type=['jpeg','jpg','png'])

file_image = st.camera_input(label = "Snap a picture 📷")

if file_image:
    input_img = Image.open(file_image)
    feed_img = input_img
    stream = io.BytesIO()
    feed_img.save(stream, format="JPEG")
    stream.seek(0)

    feed_image_data = base64.b64encode(stream.getvalue()).decode('utf-8')

    one, two = st.columns(2)
    with one:
        st.write("**Input Photo**")
        st.image(input_img, use_column_width=True)

    # POST API request
    response = requests.post(f"{BASE_URL}/api/objectrecognition/processimage", json={"image": feed_image_data})
    if response.status_code == 200:
        res_data = response.content.decode('utf-8')
        json_data = json.loads(res_data)

    # Image Format Conversion
    base64_image = json_data['image']
    image_bytes = base64.b64decode(base64_image)
    image_buffer = io.BytesIO(image_bytes)
    result_img = Image.open(image_buffer)

    # Response Data Modelling
    obj_dict = json_data['metadata']['objects']
    similarity_response = json_data['metadata']['clusters']

    # Streamlit Response Frontend
    with two:
        st.write("**Output Image**")
        st.image(result_img, use_column_width=True)

    if st.button("Download Output Image"):
        im_pil = Image.fromarray(result_img)
        im_pil.save('final_image.jpeg')
        st.write('Download completed')

    st.subheader('Objects Recognized')
    st.write(obj_dict)

    # Define column labels
    columns = ["Object", "Accuracy", "Coordinates"]

    # Convert the list into a DataFrame
    df = pd.DataFrame(obj_dict, columns=columns)

    # Display the DataFrame as a Streamlit table
    st.table(df)

    st.divider()
    st.subheader('Classified Industries')
    st.write(similarity_response)
  
    # Convert data dictionary to a pandas DataFrame
    df2 = pd.DataFrame([(obj, ', '.join(categories)) for obj, categories in similarity_response.items()], columns=["Object", "Industries"])

    # Display the table using st.dataframe()
    st.write("Object and Industries Table")
    st.dataframe(df2)

    st.divider()

    #object_list = df2["Object"].tolist()

    first_elements_list = [industry_list.split(',')[0] for industry_list in df2["Industries"]]

    first_elements_list = list(set(first_elements_list))
    
    base_url = f"{BASE_URL}/api/objectrecognition/getcompanies/"

    # print(first_elements_list)

    df3 = pd.DataFrame(columns=['Industry', 'Companies'])

    for industry in first_elements_list:

        encoded_url_part = quote(industry.strip())
        full_url = base_url + encoded_url_part

        # GET API request
        response = requests.get(full_url)
        if response.status_code == 200:
            res_data2 = response.content.decode('utf-8')
            json_data2 = json.loads(res_data2)

            data_top5 = {key: value[:5] for key, value in json_data2.items()}
            # Convert the JSON data to a Pandas DataFrame
    
            industry, companies = list(data_top5.items())[0]
            df3 = df3.append({'Industry': industry, 'Companies': companies}, ignore_index=True)

            
    # Streamlit
    st.subheader('Classified Companies')
    st.write('Industry and Companies Table')
    st.table(df3)


    st.divider()
else:
     st.write("You haven't uploaded any image file")