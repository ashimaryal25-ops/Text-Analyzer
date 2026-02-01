import io
import streamlit as st
from PyPDF2 import PdfReader
from wordcloud import WordCloud
from wordcloud import STOPWORDS
import matplotlib.pyplot as plt

st.set_page_config(page_title="PDF Word Cloud Generator")
st.title("☁️ PDF Word Cloud Creator")

# File Uploader
uploaded_file = st.file_uploader("Upload your PDF file", type="pdf")



custom_stopwords = {
    "ebscohost", "ebsco", "printed", "ebook", "collection", "https", "http",
    "www", "pdf", "page", "UTC"
}

stopwords = STOPWORDS.union(custom_stopwords)

if uploaded_file is not None:
    # Extract Text from PDF
    with st.spinner('Extracting text...'):
        reader = PdfReader(uploaded_file)
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text()
    
    if full_text.strip():
        # Generate Word Cloud
        wc = WordCloud(
            background_color="white",
            width=800,
            height=400,
            colormap='viridis',
            stopwords = stopwords
        ).generate(full_text)

        # Display using Matplotlib
        fig, ax = plt.subplots()
        ax.imshow(wc, interpolation='bilinear')
        ax.axis("off")

        st.subheader("Word Cloud:")
        st.pyplot(fig)

        # Save the WordCloud image to a buffer
        img_buffer = io.BytesIO()
        wc.to_image().save(img_buffer, format='PNG')
        byte_im = img_buffer.getvalue()

        # 2. Create the Download Button
        st.download_button(
            label="Download Word Cloud as PNG",
            data=byte_im,
            file_name="word_cloud.png",
            mime="image/png"
        )

    else:
        st.error("Could not find any text in that PDF.")