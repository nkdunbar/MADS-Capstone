import numpy as np

def clean_df(df, columns):
    df = df.drop(columns=columns)
    
    # Replace coded missing values
    df = df.replace(-9, np.nan) 
    
    df_drop = df.dropna()
    print(f'Values dropped: {len(df) - len(df_drop)}')
    
    print(f'States lost: {len(df["STFIPS"].unique()) - len(df_drop["STFIPS"].unique())}')
    
    return df_drop
    

def compute_LOS_norm(df):
    return df.groupby('SERVICES').apply(lambda grp: 
                                         grp.assign(LOSnorm=grp['LOS'] / 
                                                    grp['LOS'].mean())).reset_index(drop=True)
