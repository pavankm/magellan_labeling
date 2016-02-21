import model
def get_summary():
    result_df=model.get_label('yes')
    print(result_df,len(result_df))

get_summary()
