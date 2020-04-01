import { groundStations, GroundStation, StationName } from "./model";
import { showCursorLabel } from "./cursor_label";
// import { flyCameraToGS } from "./utils";

// This is Tomek's private token generated when signed up for Cesium.
// cspell: disable-next-line
Cesium.Ion.defaultAccessToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI4YmI1YmYxNC0xY2Q3LTQ0NjctODU5My04YWIxMDEwOWRkNTgiLCJpZCI6MTY2NTMsInNjb3BlcyI6WyJhc3IiLCJnYyJdLCJpYXQiOjE1NzA4ODgxNTF9.30hjTWZfohYJ4bNOy1DRjCeqhb2ldJ_Vze5uVWeke5Y';

// STEP 0: CREATE CESIUM WIDGET
var rectangle = Cesium.Rectangle.fromDegrees(14,51,21,54);
Cesium.Camera.DEFAULT_VIEW_RECTANGLE = rectangle;
Cesium.Camera.DEFAULT_VIEW_FACTOR = 3;

// This creates the top-level widget for Cesium.
// It has one parameter: terrainProvider, which creates terrain. Without it, the Earth surface would be completely flat.
export const viewer = new Cesium.Viewer('cesiumContainer', {
    //terrainProvider: Cesium.createWorldTerrain(),
    infoBox : true,
    selectionIndicator : true,
    shadows : true,
    shouldAnimate : true
});

showCursorLabel(viewer);

viewer.dataSources.add(Cesium.CzmlDataSource.load('czml/satnogs-fixed.czml'));
viewer.dataSources.add(Cesium.CzmlDataSource.load('czml/ground-stations.czml'));

// This function is called when Move camera button is pressed.
// @param string airport
export function flyCameraToGS(viewer: Cesium.Viewer, airport: GroundStation): void {

    const destCartographic = airport.toCartographic();
    destCartographic.height += 1500;
    const dest = Cesium.Ellipsoid.WGS84.cartographicToCartesian(destCartographic);

    viewer.camera.flyTo({
        destination : dest
    });

    // We should also stop tracking any existing objects (if any)
    viewer.trackedEntity = undefined;

    processCzml(viewer);
}

export function flyCameraZoomOut(viewer: Cesium.Viewer) {
    viewer.trackedEntity = undefined;
    viewer.camera.flyTo({
        destination: Cesium.Cartesian3.fromDegrees(18.57, 54.33, 20000000),
        duration: 3,

    });
}

export function updateButtons(viewer: Cesium.Viewer) {

    // This updates Go to airport buttons
    const flyToAirportButtons = [...document.querySelectorAll(".button-fly-to")] as HTMLButtonElement[];
    flyToAirportButtons.forEach(btn => {
        const name = btn.dataset["name"] as string;

        if (name == "globe") {
            btn.onclick = () => flyCameraZoomOut(viewer);
            return;
        }

        let dst : GroundStation;
        if (name == "tkis-1") {
            dst = new GroundStation(
                {
                    elevation: 100000,
                    latitude: 54.379,
                    longitude: 18.467,
                    name: "GDN"
                });
        }
        if (name == "eti-1") {
            dst = new GroundStation(
                {
                    elevation: 100000,
                    latitude: 54.379,
                    longitude: 18.467,
                    name: "GDN"
                });
        }

        btn.onclick = () => flyCameraToGS(viewer, dst);
    });
}


updateButtons(viewer);

