## K-means fns 


def get_kmeans_model(df, k):
    """
        k = number of clusters
    """
    return KMeans(n_clusters = k).fit(df)

def get_kmeans_labels(df, kmeans_models):
    return kmeans_models.predict(df)

def get_cdist(df, clust_centers):
    return (cdist(df, clust_centers, 'euclidean'))  # axis = 1

def find_np_min(df, clust_centers):
    return (np.min(get_cdist(df, clust_centers)), 1)

def sum_np_min_cdist(df, clust_centers):
    return [sum(find_np_min(df, clust_centers)) / df.shape[0]]

def get_kmeans_distortions(df, kmeans_model):
    #return (sum(np.min(cdist(df, kmeans_models.cluster_centers_, 'euclidean'), axis = 1)) / df.shape[0])
    return sum_np_min_cdist(df, kmeans_model.cluster_centers_)

def return_cluster_indices(kmeans_model, k):
    """
        k = cluster number to check 
        kmeans_model = (after KMeans(...).fit(df)) predicted labels on data (i.e. df)
        
        This function can be used to return the indices of our original data 
        that kmeans_model predicted to be of cluster-id = k 
        
        E.g. > return_cluster_indices(3, kmeans_model) 
        
            Will return the indices of the original data that were clustered 
            to cluster-id = 3 (i.e. the 3rd cluster of K clusters total)
    """
    return (np.where(k == kmeans_model.labels_)[0])

def return_n_kmeans(df, n = 5):
    """
        n = number of k-means models to generate
            with number-of-clusters from 1:n 
            
        This function returns a 2-d array: 
            index-0 | k-means model 
            index-1 | respective labels of model on data (predict)
            index-2 | respective cluster centroid distances (distortions)
    """
    k_models = []
    model_predicts = []
    distortions = []
    n_iters = range(1, n)
    for k in n_iters:
        print(k)
        
        ## Generate kmeans for number-of-clusters = k
        k_models.append(get_kmeans_model(df, k))
        
        ## Predict kth kmeans model on data 
        model_predicts.append(get_kmeans_labels(df, k_models[(k - 1)]))
        
        ## Calculate cluster centroid distances (distortions)
        distortions.append(get_kmeans_distortions(df, k_models[(k - 1)]))
        
    return [k_models, model_predicts, distortions]
        
########################################
