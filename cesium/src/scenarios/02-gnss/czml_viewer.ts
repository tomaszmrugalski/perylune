
// These are recommended parameters for initializng the default view. Make sure they're set before
// the viewer object is created.
//
// var rectangle = Cesium.Rectangle.fromDegrees(14,51,21,54);
// Cesium.Camera.DEFAULT_VIEW_RECTANGLE = rectangle;
// Cesium.Camera.DEFAULT_VIEW_FACTOR = 10;

import { viewerPerformanceWatchdogMixin } from "../../../typings/cesium";


export function czmlViewer(viewer: Cesium.Viewer) {

    // This updates costellation buttons
    const czmlButtons = [...document.querySelectorAll(".button-czml-load")] as HTMLButtonElement[];
    czmlButtons.forEach(btn => {
        const f = btn.dataset["file"] as string;

        btn.onclick = () => loadCzml(viewer, f);
    });

    // Find all clear-all buttons
    const clearButtons = [...document.querySelectorAll(".button-clear-all")] as HTMLButtonElement[];
    clearButtons.forEach(btn => {
        btn.onclick = () => {
            viewer.dataSources.removeAll();
        }
    })
}

function loadCzml(viewer: Cesium.Viewer, czml: string) {
    var czmlDataSource = new Cesium.CzmlDataSource();
    viewer.dataSources.add(czmlDataSource);
    czmlDataSource.load(czml);
}

