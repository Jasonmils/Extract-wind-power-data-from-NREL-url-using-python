# NREL - wind power datasets in the US
It is a national record of all the wind farms including features like power, wind speed, density, etc. However, it might be hard to doownload to total datasets from the [NREL website](https://www.nrel.gov/grid/eastern-western-wind-data.html), due to the fact that the total data size reaches the 2.9TB, which is not memory-friendly.

Hence, we have developed a python script to extract the specific wind data from the url.

First, we need to download [pywtk](https://github.com/NREL/pywtk) package. In our settings we use anaconda prompt to download  [pywtk](https://github.com/NREL/pywtk).
``` 
cd D:\pywtk  # it should be changed to your own directory of the downloaded github zip from the pywtk link
python setup.py install
```

Second, open our master-branch as a pycharm project and run `Fetch_data.py`

In this file, we can set the default url as: 

``` python
WTK_URL = "https://f9g6p4cbvi.execute-api.us-west-2.amazonaws.com/prod"
```

Then, we can select a polygon region (Longitude and Latitude) as follows to access the wind farm data within this region.
``` python
Selected_loc = ["POLYGON((-123 42, -121.25 42,  -121.5 41.2 , -123 41.2, -123 42))",  
                "POLYGON((-114 32, -115 32,  -115 34 "  
                ", -114 34, -114 32))"]
Selected_idx = ['NW', 'SE']  
Selected_region = dict(zip(Selected_idx, Selected_loc))
```
In this cases, we plot 3792 wind farm data in California, with color varing with the id of each farm. (e.g., farm id: 12305)

![windfarm](/fig/CA_windfram.png)

Then, we can access the basic information by using the `get_nc_data_from_url` function.
``` python
for region in Selected_idx:  
    sites_selected[region] = get_3tiersites_from_wkt(Selected_region[region])
```

To extract the speific wnid power data from the url with corresponding timestamps and save them as `csv`, we can use the following operation:

``` python
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

```

