# whosonfirst-www-iamhere

![](images/whosonfirst-www-iamhere.png)

`whosonfirst-www-iamhere` is a small web application for displaying coordinates based on the position of the map. Plus Who's on First data, optionally.

## Usage

### start.py - aka "fancy" mode in disguise

From this directory run the [bin/start.py](bin/start.py) command from the command line. This will start all the pieces needed to run `whosonfirst-www-iamhere` in "fancy" mode (which is [described in detail](https://github.com/whosonfirst/whosonfirst-www-iamhere/tree/master#fancy-mode) below).

Using `start.py` will require a few things that are outside the scope of this document:

1. That you know what the command line is and are comfortable using it.
2. That you have a copy of Python installed on your computer. If you are using Linux or a Mac it comes pre-installed.
3. That you have some or all of the [whosonfirst-data](https://github.com/whosonfirst/whosonfirst-data) on your computer. _This is discussed further below._

Assuming those things all you should need to do to get started is type the following from the command line:

```
$> ./bin/start.py -d /path/to/your/whosonfirst-data/data /path/to/your/whosonfirst-data/meta/wof-neighbourhood-latest.csv /path/to/your/whosonfirst-data/meta/wof-locality-latest.csv
```

See the way you are passing one or more "meta" files? Those are just CSV files included in the `whosonfirst-data` repository with pointers to Who's On First records of a particular placetype. You can pass as many "meta" files as you want. Each record in each each meta file will be indexed and be query-able by `whosonfirst-www-iamhere`.

After you run `start.py` you should start to see a lot of logging sent to your terminal as the point-in-polygon server indexes your Who's On First data. Depending on how many meta files you've chosen to index and how many records they contain (and what kind of computer you're using) this process can take between 30 seconds to three or four minutes to complete.

_A few words about the data: There is a lot of it. The entirety of the Who's On First dataset is quite large and maybe you don't need or want to download all of it just to get started with `whosonfirst-www-iamhere`._

The `start.py` script allows you to download and store only those records listed in a "meta" file before it starts all the other processes. You do this by passing the `-f` flag, for example:

```
$> curl -o wof-region-latest.csv https://raw.githubusercontent.com/whosonfirst/whosonfirst-data/master/meta/wof-region-latest.csv
$> ./bin/start.py -f -d /path/where/to/store/whosonfirst-data/ wof-region-latest.csv
```

In the example above the first thing you do is download the `wof-region-latest.csv` meta file from the [whosonfirst-data](https://github.com/whosonfirst/whosonfirst-data) repository. The `start.py` script does not support fetching remote meta files as of this writing. The next step is to run the `start.py` like usual but specifying the `-f` flag. You can specify as many meta files as you want.

The `-f` flag with instruct the `start.py` application to spawn a separate application that downloads the data (listed in the meta file) using 24 concurrent processes but depending on how many records it needs to fetch it may take a few minutes to complete. After it's cloned all the data to your computer then the `start.py` application will move along to the next step which is to index all the data.

Once all these steps have completed point your web browser to `http://localhost:8001/` and start looking around!

### "simple" mode - the basics

There is one thing you need to run `whosonfirst-www-iamhere` locally in "simple" mode. Simple mode just means a map with live-updating information about its position.

* An HTTP file server for the `whosonfirst-www-iamhere` itself. This is because some browsers are super conservative about what can and can't run on `localhost` (aka your local machine) and what can be served from a `file://` URL (aka your hard drive). In our case that means the [tangram.js](https://github.com/tangrams/tangram) library for rendering maps need to be "served" from an actual web server. A very simple HTTP file server is included in this repository and discussed more in detail below.

### "simple" mode - the details

Surprise! There is also a second moving piece, which is a local (Javascript) settings file that you will need to configure by hand. Conveniently there is a sample version in the `www/javascript` folder. If you just want to use the default settings simply make a copy of the `mapzen.whosonfirst.config.js.example` and rename it as `mapzen.whosonfirst.config.js`.

### "fancy" mode - the basics

There are four separate components to running `whosonfirst-www-iamhere` locally in "fancy" mode. Fancy mode means a map with live-updating information about its position that will reverse-geocode those coordinates and display their corresponding Who's On First polygons. Optionally, you can also enable searching for a specific place using the [Mapzen Search API](https://mapzen.com/projects/search).

They are:

* An HTTP file server for the `whosonfirst-www-iamhere` itself. This is because some browsers are super conservative about what can and can't run on `localhost` (aka your local machine) and what can be served from a `file://` URL (aka your hard drive). In our case that means the [tangram.js](https://github.com/tangrams/tangram) library for rendering maps need to be "served" from an actual web server. A very simple HTTP file server is included in this repository and discussed more in detail below.

* An HTTP file server (that can set `CORS` headers) for the serving Who's On First data. _This is discussed further below._

* The [go-whosonfirst-pip](https://github.com/whosonfirst/go-whosonfirst-pip) point-in-polygon server used to query the data.  _This is discussed further below._

* A copy of the [whosonfirst-data](https://github.com/whosonfirst/whosonfirst-data) repository. You don't actually need all of the data. You just need all of the files listed in the CSV file(s) that the point-in-polygon server needs to load in folder organized in the standard Who's On First `123/456/7/1234567.geojson` tree structure.

### "fancy" mode - the details

#### mapzen.whosonfirst.config.js

In the `www/javascript` folder there is a file called `mapzen.whosonfirst.config.js.example`. Make a copy of it called `mapzen.whosonfirst.config.js`. That's it. Unless you need or want to tailor anything to your needs. Available knobs include:

* Specifying a different endpoint for the point-in-polygon server
* Specifying a different endpoint for the Who's on First data server
* Specifying a [Pelias API key](https://mapzen.com/projects/search) if you want to enabled geocoding
* Specifying a different endpoint for the Pelias (Mapzen Search) API (for example if you're running your own instance)
* Toggling whether or not to display verbose logging in the web application

The `mapzen.whosonfirst.config.js` file is explicitly excluded from being checked-in to the `whosonfirst-www-iamhere` repository.

#### wof-pip-server

This is a small application written in the `Go` programming language that exposes point-in-polygon functionality over an HTTP API and is part of the [go-whosonfirst-pip](https://github.com/whosonfirst/go-whosonfirst-pip/) repository. _Pre-compiled binary versions of `wof-pip-server` are available for three operating systems (OS X, Linux and Windows) in the [bin](bin) directory._

```
$> ./bin/osx/wof-pip-server -port 8080 -cors -data /usr/local/mapzen/whosonfirst-data/data /usr/local/mapzen/whosonfirst-data/meta/wof-neighbourhood-latest.csv /usr/local/mapzen/whosonfirst-data/meta/wof-marinearea-latest.csv 
```

By default everything in this repository assumes the point-in-polygon server is running on port `8080`. If you change that you will need to update the `mapzen.whosonfirst.pip.endpoint` setting in config file, described below.

#### data server

This can be anything you want it to be, really, just as long as the data is returned with the `CORS` headers enabled.

We have written a small HTTP-based static webserver in the `Go` programming language called `wof-fileserver` that is part of the [go-whosonfirst-fileserver](https://github.com/whosonfirst/go-whosonfirst-fileserver) repository. _Pre-compiled binary versions of `wof-fileservers` are available for three operating systems (OS X, Linux and Windows) in the [bin](bin) directory._

```
$> ./bin/osx/wof-fileserver -port 9999 -path /usr/local/mapzen/whosonfirst-data/data/ -cors
```

By default everything in this repository assumes the data server is running on port `9999`. If you change that you will need to update the `mapzen.whosonfirst.data.endpoint` setting in config file, described below.

#### file server

This can be anything you want it to be. (It doesn't even have to set `CORS` headers.) We have written a small HTTP-based static webserver in the `Go` programming language called `wof-fileserver` that is part of the [go-whosonfirst-fileserver](https://github.com/whosonfirst/go-whosonfirst-fileserver) repository.  _Pre-compiled binary versions of `wof-fileserver` are available for three operating systems (OS X, Linux and Windows) in the [bin](bin) directory._

```
$> ./bin/osx/wof-fileserver -port 8001 -path /usr/local/mapzen/whosonfirst-www-iamhere/www/
```

## Non-WOF data sources

`whosonfirst-www-iamhere` is designed to work with data sources (collections of GeoJSON) other than Who's On First documents. There are some provisos:

1. Currently only GeoJSON `Feature` records are supported. You can not index `FeatureCollections` yet. I mean you could write the code to index them but the code doesn't do it for you yet.
2. Your GeoJSON `properties` dictionary has the following keys: `id`, `name` and `placetype`. The values can be anything (where "anything" means something that can be converted to an integer in the case of the `id` key).
3. Your GeoJSON `feature` dictionary has a `bbox` key that is an array of coordinates, [per the GeoJSON spec](http://geojson.org/geojson-spec.html#bounding-boxes).
4. Your GeoJSON file ends with `.geojson` (and not say `.json` or something else)

_Note: The list above has been copied over from the `go-whosonfirst-pip` package which does the actual point-in-polygon heavy lifting. You should always consult the [list of the provisos document there](https://github.com/whosonfirst/go-whosonfirst-pip/blob/master/README.md#using-this-with-other-data-sources) for current restrictions on using non-WOF data sources._

https://github.com/whosonfirst/go-whosonfirst-pip/blob/master/README.md#using-this-with-other-data-sources

## Shout-outs and general house-keeping

The GeoLite2 databases are distributed under the Creative Commons Attribution-ShareAlike 3.0 Unported License and are [available from MaxMind](https://dev.maxmind.com/geoip/geoip2/geolite2/).

## See also

* https://github.com/whosonfirst/whosonfirst-data
* https://github.com/whosonfirst/go-whosonfirst-pip
* https://github.com/whosonfirst/go-whosonfirst-fileserver
* https://github.com/whosonfirst/go-whosonfirst-clone
