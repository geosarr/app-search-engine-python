import streamlit as st
from utils import model, design_output, empty_result, clusters, pagination, display_duration
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from constants import MAX_NUMBER_RESULTS_PER_PAGE, PRESENTATION
from time import time


def main():


    with st.sidebar:
        st.write(PRESENTATION)
    st.title('Wikipedia Abstracts Search Engine')
    

    if "page_number" not in st.session_state:
        st.session_state["page_number"] = 0
    if "query" not in st.session_state:
        st.session_state["query"] = ""
    if "duration" not in st.session_state:
        st.session_state["duration"] = -1
    if "results" not in st.session_state:
        st.session_state["results"] = None

    query = st.text_input(label="Enter your query please : ", value="")
    time_start = time()

    if query != st.session_state.query:
        st.session_state.query = query
        st.session_state.page_number = 0
        st.session_state.duration = -1
        st.session_state.results = None

    if len(query.strip())==0:
        st.write(empty_result(), unsafe_allow_html=True)
    else:
        # st.write(f"There are {len((results))} results")
        if st.session_state.results == None:
            st.session_state.results = model.retrieval(query, clusters)
            st.session_state.duration = time() - time_start
        st.write(display_duration(st.session_state.duration), 
                 unsafe_allow_html=True
        )
        top_abstracts_urls = list(map(lambda x: (model.index.documents[x[0]].content, 
                                                 model.index.documents[x[0]].url, 
                                                 model.index.documents[x[0]].title
                                      ) , 
                                      st.session_state.results
                                     )
        )
        idx_start = st.session_state.page_number * MAX_NUMBER_RESULTS_PER_PAGE
        idx_end = (1 + st.session_state.page_number) * MAX_NUMBER_RESULTS_PER_PAGE
        results_to_show = top_abstracts_urls[idx_start : idx_end]
        st.write(design_output(results_to_show, 
                               query.split(), 
                               st.session_state.page_number
                 ), 
                 unsafe_allow_html=True
        )
        
        st.session_state.page_number = pagination(results=st.session_state.results, 
                                                  page_number=st.session_state.page_number
        )
if __name__ == '__main__':
    main()
