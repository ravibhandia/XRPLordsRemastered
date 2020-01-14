## Data manipulating + scaling fns 

def get_nine_pollut(raw_data):
    return raw_data.iloc[:, 0:9]

def log_transform_df(dat):
    return dat.apply(np.log)

def mean_normalize_df(dat):
    return (dat - dat.mean()) / dat.std()

## Scale variables (pollutants) by: (x_i - min(x)) / (max(x) - min(x))

def min_max_scaler(dat):
    scaler = preprocessing.MinMaxScaler()
    return scaler.fit_transform(dat)

## Robust scaling handles outliers by doing min-max with interquartile range

def robust_scaler(dat):
    scaler = preprocessing.RobustScaler()
    return scaler.fit_transform(dat)

## Normalizer scaling divides each value by its magnitude in n-dimensional space 
##   where n is the number of variables (i.e. pollutants)

def normalizer_scaler(dat):
    scaler = preprocessing.Normalizer()
    return scaler.fit_transform(dat)

########################################
