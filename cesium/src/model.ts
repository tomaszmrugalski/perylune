export type StationName = String;

export type VelocityUnit = "km/h" | "m/s";

export class Velocity {
    private value: number = 0;
    constructor(value: number, unit: VelocityUnit) {
        if (unit === "m/s") {
            this.value = value;
        } else {
            this.value = value * (1000 / 3600);
        }
    }
    getValue(unit: VelocityUnit) {
        if (unit === "m/s") {
            return this.value;
        } else {
            return this.value * (3600 / 1000);
        }
    }
}

export class GroundStation {
    private _name: StationName;
    private _latitude: number;
    private _longitude: number;
    private _elevation: number;

    public get name() : StationName {
        return this._name;
    }

    public get elevation(): number {
        return this._elevation;
    }

    constructor(data: {
        name: StationName;
        latitude: number;
        longitude: number;
        elevation: number;
    }) {
        this._name = data.name;
        this._latitude = data.latitude;
        this._longitude = data.longitude;
        this._elevation = data.elevation;
    }

    public toCarthesian(): Cesium.Cartesian3 {
        return Cesium.Cartesian3.fromDegrees(this._longitude, this._latitude, this._elevation);
    }

    public toCartographic(): Cesium.Cartographic {
        return Cesium.Cartographic.fromDegrees(this._longitude, this._latitude, this._elevation);
    }
}

export const groundStations: GroundStation[] = [
    // long, lat, elevation, camera height
    new GroundStation({
        elevation: 10,
        latitude: 54.379,
        longitude: 18.467,
        name: "GDN"
    }),
    new GroundStation({
        elevation: 10,
        latitude: 48.353,
        longitude: 11.778,
        name: "MUC"
    })
];
