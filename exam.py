import pandas as pd
# url = "https://www.public.com.tw/exam-civilservice/kp-quota#c"

# try:
#     #高考錄取率
#     tables = pd.read_html(url)
#     df = tables[2]
#     df.columns = df.iloc[0]
#     df = df.iloc[1:,:]
#     df.drop(df.columns[[2,3,4,5,6]], axis=1,inplace=True)
#     df.rename(columns = {'類科':'高考類科','錄取率':'高考錄取率'}, inplace = True)
#     df.to_csv('高考錄取率.csv', index=False, encoding='utf-8-sig')
#     df_saved_file = pd.read_csv('my_new_file.csv')

# except ValueError:
#     print("找不到高考錄取率")

    
#     #普考錄取率
# url2 = "https://www.public.com.tw/exam-civilservice/kp-quota#c"

# try:
#     tables2 = pd.read_html(url2)
#     df2 = tables2[3]
#     df2.columns = df2.iloc[0]
#     df2 = df2.iloc[1:,:]
#     df2.drop(df2.columns[[2,3,4,5,6]], axis=1,inplace=True)
#     df2.rename(columns = {'類科':'普考類科','錄取率':'普考錄取率'}, inplace = True)
#     df2.to_csv('普考錄取率.csv', index=False, encoding='utf-8-sig')
#     df_saved_file2 = pd.read_csv('普考錄取率')
    
    
# except ValueError:
#     print("找不到普考錄取率.")


    #薪資參考表
url_salary = "https://www.public.com.tw/exam-knowexam/civilservice-salary"

try:
    tables_salary = pd.read_html(url_salary)
    df_salary = tables_salary[0]
    df_salary.columns = df_salary.iloc[0]
    df_salary = df_salary.iloc[1:,:]
    df_salary=df_salary.drop(df_salary.index[3:]) #去處高普考之外薪資
    df_salary.to_csv('薪資參考表.csv', index=False, encoding='utf-8-sig')
    df_saved_file_salary = pd.read_csv('薪資參考表')

except ValueError:
    print("找不到薪資參考表.")