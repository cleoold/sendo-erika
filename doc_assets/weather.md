This plugin currently supports two data sources: 高德 (Amap) and OpenWeatherMap. Amap will fetch the weather data for cities in China, and OWM works for anywhere outside (in English)

A sample Chinese city search looks like:
  ```
     >> 千堂 天气 香港
        --------------------------------------
        预报时间：2019-05-29 22:51:39
        地区：香港 香港特别行政区
        2019-05-29 日：27°C，阴，无风向
        2019-05-29 夜：24°C，阵雨，无风向
        ......
  ```
Where `千堂` is my nickname. This 3-day forecast result is given by Amap. While if an English name is passed, then the result looks like:
  ```
     >> 千堂 天气 montreal
        --------------------------------------
        region: MONTREAL, CA, time diff from UTC: -4.0h
        report time: 2019-05-29 18:00:00
        2019-05-29 18:00: Clouds (overcast clouds), 16.44-17.91°C
            wind: 3.96m/s (222.787°), humidity: 65, pressure: 1004.83hPa
        2019-05-30 06:00: Clouds (broken clouds), 10.46°C
            wind: 2.46m/s (266.48°), humidity: 95, pressure: 1005.19hPa
        ......
  ```
This is given by OWM. But if you pass a Chinese string which does not correspond to a Chinese city, the translator module is activated (1000 times per day, as documented):
  ```
     >> 千堂 天气 蒙特利尔
        --------------------------------------
        region: MONTREAL, CA, time diff from UTC: -4.0h
        ......
  ```


To use this, you must request their free api keys separately.

For 高德 (Amap), go to https://lbs.amap.com/api/webservice/guide/api/weatherinfo/ and paste the key in the `API_KEY` variable in `data_source_amap.py` under `/weather` folder.

For OWM, go to https://openweathermap.org/forecast5 and paste the key in the `API_KEY` variable in `data_source_openweather.py` under `/weather` folder.