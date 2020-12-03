// This code let's changing inertial or fixed frame of reference.

import * as Cesium from "cesium";

var fixed_frame: boolean = false;

function icrf(scene: Cesium.Scene, time: Cesium.JulianDate) {
    if (scene.mode !== Cesium.SceneMode.SCENE3D) {
        return;
    }

    var icrfToFixed = Cesium.Transforms.computeIcrfToFixedMatrix(time);
    if (Cesium.defined(icrfToFixed)) {
        var camera = scene.camera;
        var offset = Cesium.Cartesian3.clone(camera.position);
        var transform = Cesium.Matrix4.fromRotationTranslation(icrfToFixed);
        camera.lookAtTransform(transform, offset);
    }
}

export function referenceFrameSelector(viewer: Cesium.Viewer): void {
    const remover = viewer.scene.postUpdate.addEventListener(icrf);
}
