import streamlit as st
from utils import model, clusters, design_output, empty_result


def main():
    st.title('Wikipedia Abstracts Search Engine')
    query = st.text_input(label="Enter your query please : ", value="")
    if len(query.strip())==0:
        st.write(empty_result(), unsafe_allow_html=True)
    else:
        results = model.retrieval(query, clusters)
        top_abstracts_urls = list(map(lambda x: (model.index.documents[x[0]].content, model.index.documents[x[0]].url, model.index.documents[x[0]].title) , results))
        st.write(design_output(top_abstracts_urls, query.split()), unsafe_allow_html=True)

if __name__ == '__main__':
    main()
