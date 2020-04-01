

export function showCursorLabel(viewer: Cesium.Viewer): void {

    // STEP 1: DISPLAY COORDS UNDER CURSOR
    // And now display the map coords under the cursor. This is strictly not needed, but it's very
    // useful for debugging.
    const coordsLabel = viewer.entities.add({
        label : {
            show : false,
            showBackground : true,
            font : '14px monospace',
            horizontalOrigin : Cesium.HorizontalOrigin.LEFT,
            verticalOrigin : Cesium.VerticalOrigin.TOP,
            pixelOffset : new Cesium.Cartesian2(15, 0)
        }
    });


    // Mouse over the globe to see the cartographic position
    const handler = new Cesium.ScreenSpaceEventHandler(viewer.scene.canvas);
    handler.setInputAction(function(movement) {
        var cartesian = viewer.camera.pickEllipsoid(movement.endPosition, viewer.scene.globe.ellipsoid);
        if (cartesian) {
            var cartographic = Cesium.Cartographic.fromCartesian(cartesian);
            var longitudeString = Cesium.Math.toDegrees(cartographic.longitude).toFixed(6);
            var latitudeString = Cesium.Math.toDegrees(cartographic.latitude).toFixed(6);

            // There's a long standing bug in Cesium about displaying labels. For the time being, This
            // is a primitive workaround: show the label 1000 meters above the ground. Looks ugly, but
            // it's enough for now.
            cartesian.z += 1000;

            coordsLabel.position = cartesian;
            coordsLabel.label.show = true;
            // coords_label.eyeOffset = new Cesium.Cartesian3(0, 0, -1000000);
            coordsLabel.label.text =
                'Lon: ' + ('   ' + longitudeString).slice(-10) + '\u00B0' +
                '\nLat: ' + ('   ' + latitudeString).slice(-10) + '\u00B0';
        } else {
            coordsLabel.label.show = false;
        }
    }, Cesium.ScreenSpaceEventType.MOUSE_MOVE);
}
