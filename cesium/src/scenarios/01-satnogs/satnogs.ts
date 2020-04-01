import { groundStations, GroundStation, StationName } from "./model";

export function run(viewer: Cesium.Viewer) {
    updateButtons(viewer);

    viewer.dataSources.add(Cesium.CzmlDataSource.load('czml/satnogs-fixed.czml'));
    viewer.dataSources.add(Cesium.CzmlDataSource.load('czml/ground-stations.czml'));
}


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


