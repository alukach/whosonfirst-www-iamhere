js: js-app js-deps

js-deps:
	cat www/javascript/leaflet.min.js www/javascript/leaflet.label.min.js  www/javascript/leaflet.hash.min.js > www/javascript/iamhere.deps.min.js

js-app:
	cat www/javascript/mapzen.whosonfirst.data.js www/javascript/mapzen.whosonfirst.log.js www/javascript/mapzen.whosonfirst.enmapify.js www/javascript/mapzen.whosonfirst.feedback.js www/javascript/mapzen.whosonfirst.geojson.js www/javascript/mapzen.whosonfirst.leaflet.js www/javascript/mapzen.whosonfirst.leaflet.styles.js www/javascript/mapzen.whosonfirst.leaflet.handlers.js www/javascript/mapzen.whosonfirst.leaflet.tangram.js www/javascript/mapzen.whosonfirst.net.js www/javascript/mapzen.whosonfirst.pelias.js www/javascript/mapzen.whosonfirst.iplookup.js www/javascript/mapzen.whosonfirst.php.js www/javascript/mapzen.whosonfirst.pip.js www/javascript/mapzen.whosonfirst.iamhere.js > www/javascript/iamhere.app.js

	java -jar utils/yuicompressor-2.4.8.jar --type js www/javascript/iamhere.app.js -o www/javascript/iamhere.app.min.js
	rm www/javascript/iamhere.app.js

css: css-deps css-app

css-deps:
	cat www/css/bootstrap.min.css www/css/leaflet.min.css www/css/leaflet.label.min.css > www/css/iamhere.deps.min.css

css-app:
	cat www/css/mapzen.whosonfirst.iamhere.css www/css/mapzen.whosonfirst.iamhere.mobile.css > www/css/iamhere.app.css
	java -jar utils/yuicompressor-2.4.8.jar --type css www/css/iamhere.app.css -o www/css/iamhere.app.min.css
	rm www/css/iamhere.app.css

mapzen:	tangram refill

tangram:
	if test -e www/javascript/tangram.js; then cp www/javascript/tangram.js www/javascript/tangram.js.bak; fi
	curl -s -o www/javascript/tangram.js https://mapzen.com/tangram/tangram.debug.js
	if test -e www/javascript/tangram.min.js; then cp www/javascript/tangram.min.js www/javascript/tangram.min.js.bak; fi
	curl -s -o www/javascript/tangram.min.js https://mapzen.com/tangram/tangram.min.js

refill:
	if test -e www/tangram/refill.yaml; then cp www/tangram/refill.yaml www/tangram/refill.yaml.bak; fi
	curl -s -o www/tangram/refill.yaml https://raw.githubusercontent.com/tangrams/refill-style/gh-pages/refill-style.yaml 
