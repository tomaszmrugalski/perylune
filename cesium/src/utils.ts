import { GroundStation, StationName } from "./model";

// This function is called when Move camera button is pressed.
// It flies to Tatry mountains.
// @param string airport
export function flyCameraTo(viewer: Cesium.Viewer, airport: GroundStation): void {

    const destCartographic = airport.toCartographic();
    destCartographic.height += 1500;
    const dest = Cesium.Ellipsoid.WGS84.cartographicToCartesian(destCartographic);

    // Sandcastle.declare(flyToSanDiego);
    viewer.camera.flyTo({
        destination : dest
    });

    // We should also stop tracking any existing objects (if any)
    viewer.trackedEntity = undefined;
}

function getVisibleValue(shouldVisible: boolean | undefined): boolean | undefined {
    if (typeof shouldVisible === 'undefined') {
        return true;
    }
    // This code alternates between undefined and false. If the property is not
    // defined, Cesium by default shows the object.
    if (!shouldVisible) {
        return false;
    } else {
        return undefined;
    }
}

// For now this is basic label that displays airport designation.
// @todo: expand this label (possibly turn this into a Billboard,
// perhaps write departures and arrivals?
export function initGroundStations(viewer: Cesium.Viewer, airports: GroundStation[]) {
    for (var airport of airports) {
      const coords = airport.toCarthesian();
      viewer.entities.add({
        position: coords,
        label : {
            showBackground : true,
            font : '14px monospace',
            horizontalOrigin : Cesium.HorizontalOrigin.LEFT,
            verticalOrigin : Cesium.VerticalOrigin.TOP,
            text: airport.name
        }
      });
    }
}

// This function formats a Date. Right now it only displays HH:MM format
// (and adds leading zeros if needed).
function formatDate(x: Date): string {
    // It was suggested to use toLocaleTimeString(), but there are several problems with that.
    // First, the toLocaleTimeString itself is supported by every major browser, but the various
    // capabilities behind it are not. See https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/toLocaleDateString#Browser_compatibility
    // Second, we don't want o have local specific formatting. We want specific HH:MM format that
    // is used around the world on every airport. Third, we don't need the locale-dependent complexity,
    // just show the basic info. We want the flights info panel to be as minimalistic as possible.
    var s: string = "";
    if (x.getHours() < 10)
        s += "0";
    s += x.getHours().toString();
    s += ':';
    if (x.getMinutes() < 10)
        s += "0";
    s += x.getMinutes().toString();

    return s;
}


