from sklearn.cluster import KMeans

def get_kmeans_clusters(features, k):
    kmeans = KMeans(init='random', n_clusters=k, n_init=features.shape[0], max_iter=300, random_state=42)
    kmeans.fit(features)
    
    # print(kmeans.labels_[:])
    
    return kmeans.labels_[:]

def merge_clusters(lex_name, cluster_dict):
    
    with open('../data/clusters/{}_clusters.csv'.format(lex_name), 'r') as rf, \
        open('../data/clusters/{}_new_clusters.csv'.format(lex_name), 'w') as wf:
            pass
        