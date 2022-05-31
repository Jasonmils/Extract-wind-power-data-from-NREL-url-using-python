# %matplotlib inline
import logging
import os
import webbrowser
import matplotlib.pyplot as plt
import io

import numpy as np
from PIL import Image
import folium
import pandas
from pywtk.site_lookup import get_3tiersites_from_wkt

# WTK_URL = "https://h2oq9ul559.execute-api.us-west-2.amazonaws.com/dev"
WTK_URL = "https://f9g6p4cbvi.execute-api.us-west-2.amazonaws.com/prod"
os.environ['PYWTK_CACHE_DIR'] = os.path.join(os.environ['USERPROFILE'], "pywtk-data")

from pywtk.wtk_api import get_nc_data_from_url

logging.basicConfig()
#
# wkt_california = "POLYGON((-124 42, -120 42," \
#                  "-120 39,-114 34,-114 32, -118 32, -124 38, -124 42)) "  # CA border
# sites = get_3tiersites_from_wkt(wkt_california)  # 28 sites info
# x = np.array(sites['lon'])
# y = np.array(sites['lat'])
# c = np.array(sites['gid'])
# # c = (c-c.min()) / (c.max()-c.min())
# plt.scatter(x, y, c=c, alpha=0.3, cmap='viridis')
# plt.colorbar()
# plt.xlabel('longitude')
# plt.ylabel('latitude')
# plt.savefig('./CA_windfram.png', dpi=100)
# plt.show()

# select wind farm in several locations using latitude
Selected_loc = ["POLYGON((-123 42, -121.25 42,  -121.5 41.2 , -123 41.2, -123 42))",
                "POLYGON((-114 32, -115 32,  -115 34 "
                ", -114 34, -114 32))"]
Selected_idx = ['NW', 'SE']
Selected_region = dict(zip(Selected_idx, Selected_loc))

sites_selected = {}

for region in Selected_idx:
    sites_selected[region] = get_3tiersites_from_wkt(Selected_region[region])
    # x_1 = np.array(sites_selected[region]['lon'])
    # y_1 = np.array(sites_selected[region]['lat'])
    # c_1 = np.array(sites_selected[region]['gid'])
    # # c = (c-c.min()) / (c.max()-c.min())
    # plt.scatter(x_1, y_1, c=c_1, alpha=0.3, cmap='viridis')
    # plt.colorbar()
    # plt.xlabel('longitude')
    # plt.ylabel('latitude')
    # plt.savefig('./CA_windfram_' + str(region) + '.png', dpi=100)
    # plt.show()

attributes = ["power", "wind_direction", "wind_speed", "temperature",
              "pressure", "density"]

# # attributes = ["power"]
leap_day = True
utc = True
# site_pack = str(sites.index)
start = pandas.Timestamp('2013-01-01', tz='utc')
end = pandas.Timestamp('2014-01-01', tz='utc')

wind_data_ensemble = {}

Selected_idx_se = ['SE']

for region in Selected_idx:
    # extract the gid from the
    gid_index = np.array(sites_selected[region]['gid'])
    count = 0
    for gid in gid_index:
        count+=1
        wind_data_ensemble[region + 'gid_' + str(gid)] = get_nc_data_from_url(WTK_URL + "/met", str(gid), start, end,
                                                                              attributes=attributes, leap_day=leap_day,
                                                                              utc=utc)
        wind_data_ensemble[region + 'gid_' + str(gid)].to_csv(
            './Data_windfarm/2013_2014/' + str(start.year) + str(end.year) + region + '_id_' + str(gid) + '.csv',
            sep=',')

        print('|| The wind farm {} is downloaded || >>>> {}/{} '.format(gid, count, len(gid_index)))

# wind_data = get_nc_data_from_url(WTK_URL + "/met", '13225', start, end, attributes=attributes, leap_day=leap_day,
#                                  utc=utc)
# wind_data['power'].plot()
