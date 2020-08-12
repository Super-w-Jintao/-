import pandas as pd
import matplotlib.pyplot as plt

#避免后续SettingWithCopyWarning的出现，影响观感
pd.set_option('mode.chained_assignment', None)

#数据写入
app_table= pd.read_csv("17 w1_applestore.csv")

# 查看表格的列参数有哪些
#print(app_table.columns)

#查看表格中APP评分数量一列的各项指标情况
rating=app_table['rating_count_tot']
#print(rating.describe())

#为排除评分数量少致评分波动大存在不真实性情况，选取1000评分人数进行过滤APP不作参考
app_table=app_table[rating>1000]
#print(len(app_table))  经筛选还剩2600个APP

#为方便观察，舍弃不要的列数据
app_table.index=app_table['id']
app_table=app_table.drop(['Unnamed: 0','id'],axis=1)

#查找热门十大APP（因数据有限，考虑以评分人数为因素）
hot_apps=app_table[['track_name','rating_count_tot']].sort_values(by='rating_count_tot',ascending=False)
hot_apps[:10].plot(kind='bar',title='Top 10 popular apps',x='track_name',color='k')
plt.show()

#查找口碑最好的十大APP （因数据有限，考虑以分数（5分上限）为基准，评分人数为因素）
columns=['track_name','user_rating','rating_count_tot']
best_reputation=app_table[columns].sort_values(by=['user_rating','rating_count_tot'],ascending=False)
best_reputation[:10].plot(kind='barh',title='Top10 apps with the best reputation',
                          fontsize='8',x='track_name',y='rating_count_tot' )
plt.show()

#查找同时位于口碑最好前500与热门前500的APP，设定为优秀APP
best500=best_reputation[:500]
hot500=hot_apps[:500]

hot_best_apps=pd.merge(best500,hot500,how='inner',on='track_name')
hb_app_name=hot_best_apps['track_name']
#print(hb_app_name)  经输出后结果得到了341款APP符合要求

#为探究得到341款APP类型占比，将其他APP数据过滤
hb_appstable=pd.merge(hb_app_name,app_table,how='inner',on='track_name')

#341款APP的类型分布情况
app_type=hb_appstable.groupby(by='prime_genre')['track_name'].count()
app_type.name='type_count'
app_type.plot(title="App type",kind='barh',color='gray',legend=True)
#print(app_type) #游戏占主体 238款
plt.show()

#类型为游戏的优秀APP中各项参数指标（支持语言数/app提供截屏数/支持IOS设备数）分布
game_table=hb_appstable[hb_appstable['prime_genre']=='Games']

lang=game_table.groupby('lang')['track_name'].count()
lang.name='lang_count'
lang.plot(kind='barh',legend=True,title='Support language',color='g')
#print(lang) #支持语言：多为1种语言 推测优秀游戏与支持的语言的多少没有必然联系
plt.show()

ipadSc_urls=game_table.groupby('ipadSc_urls')['track_name'].count()
ipadSc_urls.name='ipadSc_urls_count'
ipadSc_urls.plot(kind='barh',legend=True,title='Number of screenshots',color='orange')
#print(ipadSc_urls) #store上截屏数量：优秀游戏普遍占5张，推测优秀游戏与截屏数量有一定联系
plt.show()

sup_devices=game_table.groupby('sup_devices')['track_name'].count()
sup_devices.name='sup_devices_count'
sup_devices.plot(kind='barh',legend=True,title='Number of IOS devices supported',color='y')
#print(sup_devices) #支持的IOS设备数：各个范围有一定的占比，其中以37/38居多，推测优秀游戏与支持IOS设备数没有必然联系
plt.show()


#探究游戏大小分布与其价格的联系
game_table.loc[:,'size_bytes']=game_table['size_bytes']/1048576  #将游戏大小单位B改为MB
game_columns=['size_bytes']
max_size=game_table.size_bytes.max()
#print(max_size)  得知游戏大小最大为2815.8125MB

#用等差值分区将游戏APP个数进行划分
bins=pd.Series([0,500,1000,1500,2000,2500,3000])
labels=pd.cut(game_table.size_bytes,bins)
grouped=game_table.groupby(['price',labels])
result=grouped.size().unstack(0)
result.plot(kind='bar')
#print(result) #绝大部分小游戏都是免费的，可以看出用户青睐于免费的游戏较多，其中以小游戏为主
plt.show()




