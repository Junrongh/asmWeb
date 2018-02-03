import os
import numpy as np
import pandas as pd
import sqlite3
conn = sqlite3.connect('./Micrographs/info.sqlite')
cursor = conn.cursor()
sql = "select * from info"

df = pd.read_sql(sql, conn)
n = len(df)
print n

old_features_img = ['main', 'Image Code', 'Record Name', 'Short Name',
                    'Material name', 'UNS number', 'Composition', 'Condition',
                    'Condition details', 'Properties', 'Description',
                    'Photo method', 'Photo details', 'Etchant',
                    'Original magnification', 'Image number', 'Keywords',
                    'Submit date', 'ori_image', 'scaled_image']

new_features_img = ['main', 'Image_Code', 'Record_Name', 'Short_Name',
                    'Material_name', 'UNS_number', 'Composition', 'Condition',
                    'Condition_details', 'Properties', 'Description',
                    'Photo_method', 'Photo_details', 'Etchant',
                    'Original_magnification', 'Image_number', 'Keywords',
                    'Submit_date', 'ori_image', 'scaled_image']

result = pd.DataFrame(index=range(0, n), columns=new_features_img)

for i in range(0, n):
    print i
    for j in range(0, 20):
        result.loc[i][new_features_img[j]] = df.loc[i][old_features_img[j]]

result.to_sql(name='info', con=conn, if_exists='replace')
