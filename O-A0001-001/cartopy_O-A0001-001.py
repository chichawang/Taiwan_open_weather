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

ax.set_title('Temperature')
data=np.around(json_df['TEMP'].to_numpy().astype(np.float32),decimals=2)
data[data<-90.] = np.nan
cn=ax.scatter(lon,lat,transform=ccrs.PlateCarree(),zorder=10,s=5,cmap=plt.get_cmap('rainbow'),c=data,vmin=-10.,vmax=40.)
bar=plt.colorbar(mappable=cn,ax=ax)
#plt.colorbar(cn)

#plt.show()
ofilename=str(filename).split('.')[0]+'.png'
print(ofilename)
plt.savefig(ofilename,dpi=200)

bar.remove()
ax.set_title('Humidity')
ax.collections.clear()
data=np.around(json_df['HUMD'].to_numpy().astype(np.float32),decimals=2)
data[data<-90.] = np.nan
data=data*100.
cn=ax.scatter(lon,lat,transform=ccrs.PlateCarree(),zorder=10,s=5,cmap=plt.get_cmap('rainbow'),c=data,vmin=30.,vmax=100.)
bar=plt.colorbar(mappable=cn,ax=ax)
#plt.colorbar(cn)
ofilename=str(filename).split('.')[0]+'_HUMD.png'
print(ofilename)
plt.savefig(ofilename,dpi=200)

bar.remove()
ax.set_title('Pressure')
ax.collections.clear()
data=np.around(json_df['PRES'].to_numpy().astype(np.float32),decimals=2)
data[data<-0.] = np.nan
cn=ax.scatter(lon,lat,transform=ccrs.PlateCarree(),zorder=10,s=5,cmap=plt.get_cmap('rainbow'),c=data,vmin=990.,vmax=1040.)
bar=plt.colorbar(mappable=cn,ax=ax)
#plt.colorbar(cn)
ofilename=str(filename).split('.')[0]+'_PRES.png'
print(ofilename)
plt.savefig(ofilename,dpi=200)

bar.remove()
ax.set_title('Wind')
ax.collections.clear()
ws_data=np.around(json_df['WDSD'].to_numpy().astype(np.float32),decimals=2)
ws_data[ws_data<-0.] = np.nan
wd_data=np.around(json_df['WDIR'].to_numpy().astype(np.float32),decimals=2)
wd_data[wd_data<-0.] = np.nan
u_data=ws_data*np.cos(wd_data)
v_data=ws_data*np.sin(wd_data)
cn=ax.quiver(lon,lat,u_data,v_data,ws_data,transform=ccrs.PlateCarree(),
        zorder=10,cmap=plt.get_cmap('rainbow'),scale=100)
bar=plt.colorbar(mappable=cn,ax=ax)
#plt.colorbar(cn)
ofilename=str(filename).split('.')[0]+'_WSWD.png'
print(ofilename)
plt.savefig(ofilename,dpi=200)

bar.remove()
ax.collections.clear()
ax.set_title('24-hr Accumulation')
data=np.around(json_df['H_24R'].to_numpy().astype(np.float32),decimals=2)
data[data<-0.] = np.nan
cn=ax.scatter(lon,lat,transform=ccrs.PlateCarree(),zorder=10,s=5,cmap=plt.get_cmap('rainbow'),c=data,vmin=0.,vmax=300.)
bar=plt.colorbar(mappable=cn,ax=ax)
#plt.colorbar(cn)
ofilename=str(filename).split('.')[0]+'_APCP.png'
print(ofilename)
plt.savefig(ofilename,dpi=200)
