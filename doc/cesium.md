# Cesium Installation

Here's a super short version how to build Cesium with perylune:

```
cd cesium
ln -s ../data/czml
npm install
npm start
```

To build release version, do:

```
npm run build
```

and then you should get the package in dist/ directory.

Upgrading to latest cesium:

```
npm install cesium
```

Note: the labels will be shown as random garbage if firefox's resistFingerprinting feature is turned on.
