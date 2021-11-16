//const svg = d3.select("#map")
const svg = d3
    .select("#visualization")
    .append("svg")
    .attr("id", "map")
    .attr("height", "1000")
    .attr("width", "1200")

// create the map layers
const baseMap = svg.append("g").attr("id", "base_map");
const facilities = svg.append("g").attr("id", "facilities");
const mapGrid = svg.append("g").attr("id", "map_grid");
const mapLegend = svg.append("g").attr("id", "map_legend");
const simulationFacility = svg.append("g").attr("id", "simulation_facility");

let visType = "sim";
let simType = 'sa';

Promise.all([
    //d3.dsv(",", "ratings-by-country.csv"),
    d3.json("data/sf_neighborhoods.geojson"),
    d3.json("data/grid_definitions.geojson"),
    d3.json("data/current_fire_stations.geojson"),
    d3.dsv(",", "data/baseline_fca_output.csv"),
    d3.dsv(",", "data/travel_time.csv"),
    d3.dsv(",", "data/simulation_fca_output.csv"),
    d3.dsv(",", "data/baseline_response_time.csv"),
    d3.dsv(",", "data/simulation_response_time.csv")
]).then(function (data) {

    const sfMapData = data[0];
    const mapGridData = data[1];
    const sfFacilityData = data[2];
    const baselineFcaOutput = data[3];
    const travelTime = data[4];
    const simulationFcaOutput = preprocessSimulationData(data[5]);
    const baselineResponseTime = data[6];
    const simulationResponseTime = preprocessSimulationData(data[7]);

    // draws the base map
    const mapCtx = setupMap(sfMapData);

    function drawMap() {
        facilities.selectAll("*").remove();
        mapGrid.selectAll("*").remove();
        mapLegend.selectAll("*").remove();
        simulationFacility.selectAll("*").remove();

        refreshData(mapCtx, {
            sfFacilityData: sfFacilityData,
            mapGridData: mapGridData,
            baselineFcaOutput: baselineFcaOutput,
            travelTime: travelTime,
            simulationFcaOutput: simulationFcaOutput,
            baselineResponseTime: baselineResponseTime,
            simulationResponseTime: simulationResponseTime,
        });
    }

    $("#reset_fca").click(function (evt) {
        drawMap();
    });

    d3.selectAll("input[name='simulation_type']").on("change", function () {
        simType = this.value;
        drawMap();
    });

    d3.select("#dropdown").on("change", function () {
        visType = this.value;
        if (visType !== 'sim') {
            d3.select("#simulation_controls").style("display", "none");
        } else {
            d3.select("#simulation_controls").style("display", "");
            drawMap();
        }
    });

    drawMap();
});

function preprocessSimulationData(simulationData) {
    let simulations = {};
    simulationData.forEach(x => {
        const simName = x.scenario_name;
        if (!(simName in simulations)) {
            simulations[simName] = [];
        }
        simulations[simName].push(x);
    });
    return simulations;
}

function refreshData(mapCtx, data) {
    const facilities = drawFacilities(mapCtx, data.sfFacilityData);

    let gridValues = data.baselineFcaOutput;
    if (simType === 'rt') {
        gridValues = data.baselineResponseTime;
    }
    const gridDrawer = setupGridDrawer(mapCtx, data.mapGridData, gridValues);
    const mapGridCells = gridDrawer(gridValues);

    setupEventHandlers(mapCtx, data, mapGridCells, gridDrawer);
}

function setupMap(geoObj) {

    const projection = d3.geoEquirectangular()
    projection.fitExtent(
        [
            [0, 0],
            [1200, 1000],
        ],
        geoObj
    )
    const path = d3.geoPath().projection(projection)

    baseMap.selectAll("path")
        .data(geoObj.features)
        .enter()
        .append("path")
        .attr("d", (d) => path(d))
        .attr("fill", "white")
        .attr("stroke", "gray")

    return {
        projection: projection,
        path: path
    }
}

function drawFacilities(mapCtx, facilityData) {

    return facilities.selectAll("path")
        .data(facilityData.features)
        .enter()
        .append("path")
        .attr("d", (d) => mapCtx.path(d))
        .attr("fill", "red")
        .attr("stroke", "red")
}

function setupGridDrawer(mapCtx, gridDefinition, initialGridValues) {

    const valMin = d3.min(initialGridValues, x => Number.parseFloat(x.value));
    const valMax = d3.max(initialGridValues, x => Number.parseFloat(x.value));
    const valMid = d3.mean(initialGridValues, x => Number.parseFloat(x.value));

    const colorScale = d3.scaleLinear()
        .domain([valMin, valMid, valMax])
        .range(["red", "yellow", "green"]);

    // closure scoped
    var isFirstDraw = true;
    var mapGridCells = null;

    function gridDrawer(redrawGridValues) {

        if (!redrawGridValues) {
            redrawGridValues = initialGridValues
        }

        const valLookup = {}
        redrawGridValues.forEach(x => {
            valLookup[x.zone_idx] = x.value;
        })

        if (isFirstDraw) {
            mapGridCells = mapGrid.selectAll("path")
                .data(gridDefinition.features)
                .enter()
                .append("path")
                .attr("d", (d) => mapCtx.path(d))
                .attr("fill-opacity", "0.25")
                .attr("id", (d) => {
                    return "zone_idx_" + d.properties.zone_idx;
                })
                .attr("fill", (d) => {
                    const zoneIdx = d.properties.zone_idx + "";
                    const zoneVal = valLookup[zoneIdx];
                    if (!zoneVal) {
                        return "white";
                    } else {
                        return colorScale(zoneVal);
                    }
                });
            isFirstDraw = false;
        } else {
            for (let zoneIdx in valLookup) {
                d3.select("#zone_idx_" + zoneIdx)
                    .attr("fill", colorScale(valLookup[zoneIdx]));
            }
        }

        return mapGridCells;
    }

    return gridDrawer;
}

function setupEventHandlers(mapCtx, data, mapGridCells, gridDrawer) {

    const travelTimeLookup = {};
    const originalColors = {};
    const travelTime = data.travelTime;
    let simulationData = data.simulationFcaOutput;
    if (simType === 'rt') {
        simulationData = data.simulationResponseTime;
    }


    // build a lookup structure for each grid cell indicating which other cells can
    // be traveled to within 5 minutes
    travelTime.forEach((r) => {
        if (!(r.selected_zone in travelTimeLookup)) {
            travelTimeLookup[r.selected_zone + ""] = [];
        }
        travelTimeLookup[r.selected_zone + ""].push(r.covered_zone);
    });

    function resetColors() {
        let processedKeys = [];
        for (k in originalColors) {
            d3.select(k).attr("fill", originalColors[k])
            processedKeys.push(k);
        }
        processedKeys.forEach(k => delete originalColors[k])
    }

    mapGridCells.on("click", (x) => {
        const zoneIdx = x.properties.zone_idx + "";
        const simulationKey = "new_station_" + zoneIdx;

        resetColors();
        if (simulationKey in simulationData) {
            gridDrawer(simulationData[simulationKey]);
        }

        const clickCoords = {
            x: d3.event.layerX,
            y: d3.event.layerY
        }

        simulationFacility.selectAll("*").remove();

        simulationFacility
            .append("circle")
            .attr("cx", clickCoords.x)
            .attr("cy", clickCoords.y)
            .attr("fill", "blue")
            .attr("r", 6)


    }).on("mouseover", (x) => {

        resetColors();

        const zoneIdx = x.properties.zone_idx + "";
        d3.select("#zone_idx_" + zoneIdx).attr("stroke", "black");

        // color the 5 minute travel time cells
        if (zoneIdx in travelTimeLookup) {
            const elementsToColor = travelTimeLookup[zoneIdx].map(x => "#zone_idx_" + x);
            // store the original colors
            elementsToColor.forEach(x => {
                originalColors[x] = d3.select(x).attr("fill");
            })
            // update to be colored for the response area
            d3.selectAll(elementsToColor.join(","))
                .attr("fill", "purple");
        }
    }).on("mouseout", (x) => {
        let zoneIdx = x.properties.zone_idx + "";
        d3.select("#zone_idx_" + zoneIdx).attr("stroke", "none");
        resetColors();
    });
}