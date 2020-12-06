
// This code initializes existing buttons with loadCzml function. Once clicked, the buttons will load specified CZML files.
//
// Usage:
// 1. Add a button with button-czml-load class and data-file property point to the CZML file name you want to load, e.g.
//     <button class="cesium-button button-czml-load" data-file="czml/polish.czml">Polskie satelity</button>
// 2. Call czmlViewer(viewer); from your .ts file.
// 3. Now when user clicks the button, the specified CZML file will be loaded.

import * as Cesium from "cesium";

let sats : Cesium.Entity[] = [];

function addSat(sat: Cesium.Entity) {
    sats.push(sat);
}

function getSat(sat_id: string) : Cesium.Entity | undefined  {

    console.log(sats.length + " sat(s) defined.");
    let s = sats.find(sat => sat.id == sat_id);
    console.log("getSat(" + sat_id + ") returns " + s);


    return s;
}

export function czmlViewer(viewer: Cesium.Viewer) {

    // This updates constellation buttons
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

    // We should load the DataSource. The load() function returns a promise, which will eventually resolve
    // once the file is actually loaded. It will trigger the function specifide by then().
    czmlDataSource.load(czml).then(function(){
        updateUI(viewer);
        updateButtonCallbacks(viewer);

        console.log("Loaded " + sats.length + " sat(s).");
    });

}

// This function is called when the CZML data source finished loading.
function updateUI(viewer:Cesium.Viewer) {
    const dses = viewer.dataSources;
    if (dses.length < 1) {
        console.log("ERROR: No datasources loaded.");
        return;
    }

    const tableBody = document.querySelector('#satList tbody') as HTMLTableSectionElement;

    const ds = dses.get(0); // DataSource
    var entities = ds.entities.values; // Cesium.EntityCollection col;// = ds.entities;
    // ds.entities = Cesium.EntityCollection.
    console.log(entities);
    for (var i =0; i < entities.length; i++) {
        var e : Cesium.Entity = entities[i];

        var props = e.properties;

        console.log(i + ": id=" + e.id + " name=" + e.name + ", TLE=" + props);
        if (e.name === undefined) {
            continue;
        }

        addSat(e);

        const row = tableBody.insertRow();
        row.id = 'info-' + e.name;
        row.dataset['sat_id'] = e.id;
        row.dataset['sat_name'] = e.name;

        // cell 1: Sat button
        let cell = row.insertCell();
        let btn = document.createElement('button');
        btn.classList.add('cesium-button', 'button-sat-focus');
        btn.dataset['sat_id'] = e.id;
        btn.dataset['sat_name'] = e.name;
        btn.innerText = e.name;
        cell.appendChild(btn);

        let cell2 = row.insertCell();
        if (e.name == "PWSat" || e.name == "Brite-PL (Lem)") {
            cell2.classList.add("red");
            cell2.innerText = "NIE";
        } else {
            cell2.classList.add("green");
            cell2.innerText = "TAK";
        }

        let cell3 = row.insertCell();
        let btn2 = document.createElement('button');
        btn2.classList.add('cesium-button', 'button-sat-path');
        btn2.id = "button-sat-path-" + e.id;
        btn2.dataset['sat_id'] = e.id;
        btn2.dataset['sat_name'] = e.name;
        btn2.innerText = "Widoczna";
        cell3.appendChild(btn2);
    }

}

function updateButtonCallbacks(viewer: Cesium.Viewer) {

    // This updates Sat buttons
    const flyToAirportButtons = [...document.querySelectorAll(".button-sat-focus")] as HTMLButtonElement[];
    flyToAirportButtons.forEach(btn => {
        const sat_id = btn.dataset["sat_id"];
        if (sat_id === undefined) {
            return;
        }
        btn.onclick = () => focusCameraTo(viewer, sat_id);
    });

    // This updates Sat trajectory visibility buttons
    const toggleSatPathButtons = [...document.querySelectorAll(".button-sat-path")] as HTMLButtonElement[];
    toggleSatPathButtons.forEach(btn => {
        const sat_id = btn.dataset["sat_id"];
        if (sat_id === undefined) {
            return;
        }
        btn.onclick = () => toggleSatPath(viewer, sat_id);
    });

}

function focusCameraTo(viewer: Cesium.Viewer, sat_id: string) {
    console.log("focusCameraTo(.., " + sat_id + ") clicked");
    var x = getSat(sat_id);
    if (x === undefined) {
        return;
    }
    if (viewer.trackedEntity == x) {
        viewer.trackedEntity = undefined;
        viewer.selectedEntity = undefined;
    } else {
        viewer.trackedEntity = x;
        viewer.selectedEntity = x;
    }

    if (x && x.properties) {
        console.log("getting TLE for object " + x.name);
        var tle1 = x.properties["tle1"];
        var tle2 = x.properties["tle2"];

        showTLEInfo(tle1, tle2);
    } else {
        showTLEInfo("", "");
    }

}

// Shows specified TLE information in the TLE INFO window in the lower right corner.
function showTLEInfo(line1 : string, line2: string): void {
    var info = document.querySelector("#tle-info") as HTMLTableCellElement;
    info.innerText = line1 + "\n" + line2;
}

// Toggles path visibility (turns the path on or off and flips the button text)
function toggleSatPath(viewer: Cesium.Viewer, sat_id: string) {
    console.log("toggleSatPath(.., " + sat_id + ") clicked");
    var x = getSat(sat_id) as Cesium.Entity;
    if (x === undefined || x.path === undefined) {
        console.log("ERROR: Unable to find sat with sat_id=" + sat_id);
        return;
    }
    if (x.path.show) {
        x.path.show = undefined;
        var d = document.querySelector("#button-sat-path-" + sat_id) as HTMLButtonElement;
        if (d) {
            d.innerText = "Widoczna";
        }
        console.log("Hiding path [" + d + "]");
    } else {
        console.log("Showing path");
        x.path.show = new Cesium.ConstantProperty(false);
        var d = document.querySelector("#button-sat-path-" + sat_id) as HTMLButtonElement;
        if (d) {
            d.innerText = "Ukryta";
        }

    }
}