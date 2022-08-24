

def rank_documents(doc_scores, top):
    top_documents= sorted(doc_scores.items(), key=lambda item: item[1], reverse=True)[:top]
    if len(top_documents)>0:
        if top_documents[0][1]==0:
            return []
    return top_documents