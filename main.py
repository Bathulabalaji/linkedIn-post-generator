import streamlit as st
from few_shot import FewShotPosts
from generate_post import generate_post

def main():
    st.title("LinkedIn Post Generator")
    col1, col2, col3 = st.columns(3)

    fs = FewShotPosts()
    with col1:
        selected_tag = st.selectbox("Topic", options=fs.get_tags())
    with col2:
        selected_length = st.selectbox("Length", options=["Short", "Medium", "Long"])

    with col3:
        selected_language = st.selectbox("Language", options=["English", "Telugu", "Telgish"])
    if st.button("Generate", type="primary"):
        post = generate_post(selected_tag, selected_length, selected_language)
        st.write(f"Generated post for {selected_tag} tag, {selected_length} length in {selected_language} language is:")
        st.write(post)


if __name__ == "__main__":
    main()