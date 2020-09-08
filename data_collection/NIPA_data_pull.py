def bea_nipa_request(token, list_years):
    import requests
    import pandas as pd
    import time
    #########################################
    def get_LineDescription(data):
        ls = []
        for i in range(len(data['BEAAPI']['Results']['Data'])):
            des = data['BEAAPI']['Results']['Data'][i]['LineDescription']
            if des not in ls:
                ls.append(des)
            else:
                ls
        return ls
    
    #########################################
    def get_timeperiod(data):
        ls = []
        for i in range(len(data['BEAAPI']['Results']['Data'])):
            des = data['BEAAPI']['Results']['Data'][i]['TimePeriod']
            if des not in ls:
                ls.append(des)
            else:
                ls
        return ls

    ########################################
    df = pd.DataFrame()
    for i in list_years:
            base_url ='https://apps.bea.gov/api/data/'

            param = {
            'USERID': token,
            'METHOD': 'GetData',
            'DATASETNAME' : 'NIPA',
            'TableName': 'T10106',
            'Frequency' : 'Q',
            'Year' : i,   
            }

            res = requests.get(base_url, params = param)
            print(res.status_code)        

            data = res.json()

            col_list = get_LineDescription(data)
            col_timeperiod = get_timeperiod(data)

            df_pull = pd.DataFrame(data['BEAAPI']['Results']['Data'])
            df_pull.drop(columns = ['TableName', 'SeriesCode', 'LineNumber', 'METRIC_NAME', 'UNIT_MULT', 'CL_UNIT'], inplace = True)

            data = pd.DataFrame({'TimePeriod': col_timeperiod})
            for description in col_list:
                frame = df_pull.loc[df_pull['LineDescription'] == description,:].rename(columns={'DataValue':description}).drop(columns=['LineDescription']).reset_index().copy()
                data[description] = frame[description]
            df = df.append(data)
            time.sleep(6)
        
    return df
