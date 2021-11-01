def load_table(dbname="fire_data_v1.db", tableName='fire_incidents'):
    """
    load table from sqlite db
    """
    import sqlite3
    con = sqlite3.connect(dbname)
    cur = con.cursor()

    df=pd.read_sql('select * from '+tableName,con=con)
    return df

def transform_data(df):
    """
    transform data from sqlite load
    
    """

    df['alarm_format'] = pd.to_datetime(df['alarm_dttm'])

    df['arrival_format'] = pd.to_datetime(df['arrival_dttm'])

    df['arrival_time'] = (df['arrival_format'] - df['alarm_format'])
    
    df['minutes'] = (df.arrival_time.dt.seconds) / 60
    
    df['day_of_week'] = df['alarm_format'].dt.day_name().astype(str)
    
    df['dayflag'] = (df.alarm_format.dt.hour > 5) & (df.alarm_format.dt.hour <18)
    
    cols = ['minutes','alarm_format','arrival_format','day_of_week','dayflag','zipcode',\
            'battalion', 'station_area', 'ems_units', 'number_of_alarms', 'primary_situation',\
            'action_taken_primary', 'property_use', 'neighborhood_district', 'supervisor_district', 'structure_type',\
            'area_of_fire_origin','detector_type','detector_operation']
    
    return df[cols]


def split_data(df,months_excluded=3):
    """
    split data based on dates... needs improvement but getting going
    change number of months to holdout
    """
    X = df.loc[:,df.columns != 'minutes']
    y = df['minutes']
    
    date_max = max(df['alarm_format'])
    
    train_date_max = date_max - pd.DateOffset(months=months_excluded)

    
    X_train, y_train = X[X.alarm_format <= train_date_max], y[X.alarm_format <= train_date_max]
    X_test, y_test = X[X.alarm_format > train_date_max] , y[X.alarm_format > train_date_max]
    
    X_train.drop(['arrival_format','alarm_format'],axis=1,inplace=True)
    X_test.drop(['arrival_format','alarm_format'],axis=1,inplace=True)
    
    ############################### needs encoded
    lbl = preprocessing.LabelEncoder()
    
    X_train['day_of_week'] = lbl.fit_transform(X_train['day_of_week'].astype(str))
    X_train['battalion'] = lbl.fit_transform(X_train['battalion'].astype(str))
    X_train['primary_situation'] = lbl.fit_transform(X_train['primary_situation'].astype(str))
    X_train['action_taken_primary'] = lbl.fit_transform(X_train['action_taken_primary'].astype(str))
    X_train['property_use'] = lbl.fit_transform(X_train['property_use'].astype(str))
    X_train['neighborhood_district'] = lbl.fit_transform(X_train['neighborhood_district'].astype(str))
    X_train['structure_type'] = lbl.fit_transform(X_train['structure_type'].astype(str))
    X_train['area_of_fire_origin'] = lbl.fit_transform(X_train['area_of_fire_origin'].astype(str))
    X_train['detector_type'] = lbl.fit_transform(X_train['detector_type'].astype(str))
    X_train['detector_operation'] = lbl.fit_transform(X_train['detector_operation'].astype(str))
    
    X_test['day_of_week'] = lbl.fit_transform(X_test['day_of_week'].astype(str))
    X_test['battalion'] = lbl.fit_transform(X_test['battalion'].astype(str))
    X_test['primary_situation'] = lbl.fit_transform(X_test['primary_situation'].astype(str))
    X_test['action_taken_primary'] = lbl.fit_transform(X_test['action_taken_primary'].astype(str))
    X_test['property_use'] = lbl.fit_transform(X_test['property_use'].astype(str))
    X_test['neighborhood_district'] = lbl.fit_transform(X_test['neighborhood_district'].astype(str))
    X_test['structure_type'] = lbl.fit_transform(X_test['structure_type'].astype(str))
    X_test['area_of_fire_origin'] = lbl.fit_transform(X_test['area_of_fire_origin'].astype(str))
    X_test['detector_type'] = lbl.fit_transform(X_test['detector_type'].astype(str))
    X_test['detector_operation'] = lbl.fit_transform(X_test['detector_operation'].astype(str))
    ###############################
    
    return X_train, y_train, X_test, y_test


    
def show_importance(model,metric='weight'):
    """
    
    show feature importance by metric interested in, see xgboost docs for more
    
    """
    feature_important = model.get_booster().get_score(importance_type=metric)
    keys = list(feature_important.keys())
    values = list(feature_important.values())

    data = pd.DataFrame(data=values, index=keys, columns=["score"]).sort_values(by = "score", ascending=False)
    
    return data.plot(kind='barh')

def quantile_importance(df):
    """
    display quantile importance chart for each quantile of response
    """

    df['quantile']=pd.qcut(df['minutes'],10,labels=False)
    df = df[df['quantile'].notna()]

    for i in range(0,10):
        df_loop=df.loc[df['quantile']==i]
        df_loop.drop(['quantile'], axis=1)
        df_loop, res = run_model(df_loop)
        print("Quantile #"+str(i))
        show_importance(res,'gain')








def run_model(df):
    
    X_train, y_train, X_test, y_test = split_data(df)
    
    model = XGBRegressor(max_depth=3,
                     n_estimators=100,
                     min_child_weight=2,
                     learning_rate=.2)
    
    
    model.fit(X_train,y_train,verbose=False)
    
    
    y_pred = model.predict(X_test)

    df_out = pd.DataFrame()

    df_out['preds'] = y_pred
    
    return df_out, model