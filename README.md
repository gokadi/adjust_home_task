# Test task for adjust
## Description
Expose the sample dataset through a single generic HTTP API endpoint, which is capable of filtering, grouping and sorting.<br/>
Dataset represents performance metrics (impressions, clicks, installs, spend, revenue) for a given date, advertising channel, country and operating system.<br/>
Dataset is expected to be stored and processed in a relational database. 

Client of this API should be able to:
1) filter by time range (date_from+date_to is enough), channels, countries, operating systems
2) group by one or more columns: date, channel, country, operating system
3) sort by any column in ascending or descending order
4) see derived metric CPI (cost per install) which is calculated as cpi = spend / installs

## API contract
``/statistics/get_report``

GET parameters:

- ``date_from`` - %Y-%m-%d (e.g. 2012-05-29)
- ``date_to`` - %Y-%m-%d (e.g. 2012-05-29)
- ``channels`` - comma-separated list of values
- ``countries`` - comma-separated list of values
- ``os`` - comma-separated list of values
- ``group_by`` - comma-separated list of values (possible values: 'date', 'channel', 'country', 'os')
- ``order_by`` - single value ('date', 'channel', 'country', 'os', 'impressions', 'clicks', 'installs', 'spend', 'revenue') 
- ``view_mode`` - if ``download``, than the report will be downloaded as csv file. If ``ui``, table with data will be rendered.

Response is in csv format:

```
    {"report": "date,impressions,clicks,installs,spend,revenue,cpi\n2017-05-17,53012,1781,346,709.06,717.6700000000001,2.0493063583815028\n"}
```
    
Examples of usage below.
    
## Common API use-cases Links:
1) Show the number of impressions and clicks that occurred before the 1st of June 2017, broken down by channel and country, sorted by clicks in descending order. Hint:
http://127.0.0.1:8000/statistics/get_report/?date_to=2017-06-01&group_by=channel,country&order_by=-clicks
2) Show the number of installs that occurred in May of 2017 on iOS, broken down by date, sorted by date in ascending order.
http://127.0.0.1:8000/statistics/get_report/?date_from=2017-05-01&date_to=2017-06-01&os=ios&group_by=date&order_by=date
3) Show revenue, earned on June 1, 2017 in US, broken down by operating system and sorted by revenue in descending order.
http://127.0.0.1:8000/statistics/get_report/?date_from=2017-06-01&date_to=2017-06-02&group_by=os&order_by=-revenue&countries=US
4) Show CPI and spend for Canada (CA) broken down by channel ordered by CPI in descending order. Please think carefully which is an appropriate aggregate function for CPI.
http://127.0.0.1:8000/statistics/get_report/?countries=CA&group_by=channel&order_by=-cpi

## How to run locally?

Global installation:

```shell script
$ make install
$ python manage.py runserver
```

Local installation:

```shell script
$ python3 -m venv venv
$ source venv/bin/activate 
$ make install_dev
$ python manage.py runserver
```

Admin panel is accessible on /admin/, credentials:

```
username: admin
password: admin
```

Create ``.env`` file with:

```
DEBUG=True
```

otherwise admin panel wouldn't load static. 

### To run tests, you can call

```shell script
$ python3 -m venv venv
$ source venv/bin/activate 
$ make install_dev
$ make test
```

### Work with dataset

Also, you can erase the whole dataset from the DB by calling:

```shell script
$ python manage.py clear_dataset
```

And load it back again by calling:

```shell script
$ python manage.py load_dataset --from {PATH_TO_FILE_IN_CSV}
```

Note, that ``--from`` parameter is optional, by default the dataset which 
was sent with task, is loaded.


### Other notes

- currently it's implemented using basic django. If we need to extend this system it'd
  be useful to use DRF;
- some functionality is limited by tech requirements (i.e. SQLite3 doesn't support 
  some of common features);
- you can build wheels (``make build_dist``). Currently tests are included in dist
  so that you can test it from there.