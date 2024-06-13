import pandas as pd
def process(df,region_df):

    df=df[df["Season"]=="Summer"]

    df=df.merge(region_df,on="NOC",how="left")

    df.drop_duplicates(inplace=True)

    a=pd.get_dummies(df["Medal"])

    df=pd.concat([df,a],axis=1)

    # df.drop(["notes"],inplace=True,axis=1)
    return df