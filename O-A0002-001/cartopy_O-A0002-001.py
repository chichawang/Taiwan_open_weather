import cartopy
import numpy as np
import matplotlib.pyplot as plt
import sys
import pandas as pd
import json
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from   cartopy.io.shapereader import Reader
from   cartopy.feature import ShapelyFeature

#cartopy.config['data_dir']='/data-nas/share/mapsdata/'

filename=sys.argv[1]
with open(filename) as f:
  json_dict=json.loads(f.read())
json_df=pd.DataFrame(json_dict['cwbopendata']['location'])

part_df=pd.DataFrame()
for i in range(json_df.shape[0]) :
  tmp_df=pd.json_normalize(json_df['weatherElement'][i]).set_index("elementName")
  tmp_df.index.names=[None]
  tmp_df2=tmp_df.T.reset_index(drop=True)
  part_df=part_df.append(tmp_df2,ignore_index=True)

json_df=pd.concat([json_df,part_df],axis=1,sort=False)
json_df=json_df.drop(labels=['weatherElement', 'parameter'],axis="columns")

#fig = plt.figure(figsize=(8,6))
#ax=plt.axes(facecolor='0.1',projection=ccrs.PlateCarree())
fig,ax=plt.subplots(figsize=(8,6),subplot_kw={'projection':ccrs.PlateCarree()})
ax.set_extent([118.0,123.0,21.0,27.0])
land=cfeature.NaturalEarthFeature('physical','land','10m',
     edgecolor='gray',facecolor='0.2')
sea=cfeature.NaturalEarthFeature('physical','ocean','10m',
     edgecolor='gray',facecolor='0.1')
ax.add_feature(land)
ax.add_feature(sea)
xlabels=[119,120,121,122,123]
ylabels=[21,22,23,24,25,26,27]
ax.gridlines(draw_labels="Fasle", alpha=0.2,
             xlocs=xlabels,
             ylocs=ylabels)
sss=Reader("../shp_file/COUNTY_MOI_1090820.shp")
ax.add_geometries(sss.geometries(),
                  ccrs.PlateCarree(),
                  facecolor='none',linewidth=0.3,edgecolor='0.6')
lon=np.around(json_df['lon'].to_numpy().astype(np.float32),decimals=2)
lat=np.around(json_df['lat'].to_numpy().astype(np.float32),decimals=2)

ax.set_title('Rainfall')
data24=np.around(json_df['HOUR_24'].to_numpy().astype(np.float32),decimals=2)
data24[data24<-90.] = np.nan
data3=np.around(json_df['HOUR_3'].to_numpy().astype(np.float32),decimals=1)
data3[data3<-90.] = np.nan
data1=np.around(json_df['RAIN'].to_numpy().astype(np.float32),decimals=1)
data1[data1<-90.] = np.nan

sizes=data1
marks=data1
size=1
marks='o'

for ii in range(0,json_df.shape[0]-1):
    if data1[ii] > 40:
      size[ii]=5
    if data24[ii] > 80 :
      size[ii]=5
    elif data24[ii] > 200:
      size[ii]=8
      marks[ii]='^'
    elif data24[ii] > 350:
      size[ii]=11
      marks[ii]='^'
    elif data24[ii] > 500:
      size[ii]=14
      marks[ii]='^'
    if data3[ii] > 100:
      size[ii]=8
      marks[ii]='^'
    elif data3[ii] > 200:
      size[ii]=11
      marks[ii]='^'

cn=ax.scatter(lon,lat,transform=ccrs.PlateCarree(),zorder=10,s=size,marker=marks,cmap=plt.get_cmap('rainbow'),c=data24,vmin=-1.,vmax=100.)
bar=plt.colorbar(mappable=cn,ax=ax)
#plt.colorbar(cn)

#plt.show()
ofilename=str(filename).split('.')[0]+'.png'
print(ofilename)
plt.savefig(ofilename,dpi=200)
