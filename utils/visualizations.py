## Data viz fns 

def show_beautiful_bivariate_groupings(dat, color_by = False):
    g = sns.PairGrid(dat, hue = color_by)
    g.map_diag(plt.hist)
    g.map_offdiag(plt.scatter)
    g.add_legend();
    
def show_correlation_heatmap(corr_matrix):
    fig, ax = plt.subplots(figsize = (12, 12))  
    ax = sns.heatmap(corr_matrix, annot = True, linewidths = 1, ax = ax, cmap = "Reds")
    fig = ax.get_figure()

## Make boxplot of single column 

def show_col_boxplot(df, col):
    fig = plt.figure(figsize = (8, 8))
    ax = fig.gca()
    df.boxplot(column = col, ax = ax)
    ax.set_title("Filtered column: " + col)
    #ax.set_xlabel(col)
    ax.set_ylabel("Values")
    return "show_col_boxplot() for " + col

def get_each_col_boxplot(df, col_names):
    ## List comprehension (call fn on each item in list)
    # [fn_to_call() for item in the_list]
    return [show_col_boxplot(df, col_name) for col_name in col_names]
