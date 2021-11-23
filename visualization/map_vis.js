//const svg = d3.select("#map")
const svg = d3
    .select("#visualization")
    .append("svg")
    .attr("id", "map")
    .attr("height", "1000")
    .attr("width", "1200")
    .attr("style", "background-color: e5f0f9; margin-left: 50px;")

const svgLegend = d3
    .select("#visualization_legend")
    .append("svg")
    .attr("height", "300")
    .attr("width", "600")

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
    d3.dsv(",", "data/simulation_response_time.csv"),
    d3.dsv(",", "data/demand.csv"),
    d3.dsv(",", "data/supply_data.csv")
]).then(function (data) {

    const sfMapData = data[0];
    const mapGridData = data[1];
    const sfFacilityData = data[2];
    const baselineFcaOutput = data[3];
    const travelTime = data[4];
    const simulationFcaOutput = preprocessSimulationData(data[5]);
    const baselineResponseTime = data[6];
    const simulationResponseTime = preprocessSimulationData(data[7]);
    const demandData = data[8];
    const supplyData = data[9];

    // draws the base map
    const mapCtx = setupMap(sfMapData);

    function drawMap() {
        facilities.selectAll("*").remove();
        mapGrid.selectAll("*").remove();
        mapLegend.selectAll("*").remove();
        simulationFacility.selectAll("*").remove();

        drawSimulationLegend();

        refreshData(mapCtx, {
            sfFacilityData: sfFacilityData,
            mapGridData: mapGridData,
            baselineFcaOutput: baselineFcaOutput,
            travelTime: travelTime,
            simulationFcaOutput: simulationFcaOutput,
            baselineResponseTime: baselineResponseTime,
            simulationResponseTime: simulationResponseTime,
            demandData: demandData,
            supplyData: supplyData
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
        if (visType === 'sim') {
            d3.select("#simulation_controls").style("display", "");
            drawMap();
        } else {
            d3.select("#simulation_controls").style("display", "none");
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

/*
  Rather than precomputing everything for everywhere the user could click, this function
  uses "partial application" (in the functional programming sense) to compute values "just-in-time".
*/
function createTooltipDataProcessor(baselineFcaOutput, simulationFcaOutput, demandDataRaw, supplyDataRaw) {

    // shallow copy the data, and merge it all together
    const allData = Object.assign({}, simulationFcaOutput);
    allData["baseline"] = baselineFcaOutput;

    // process the demand data into a lookup table w/ numeric values
    const demandData = {};
    demandDataRaw.forEach(demandRow => {
        demandData[demandRow.zone_idx] = Number.parseFloat(demandRow.number_of_calls);
    });

    const supplyData = {};
    supplyDataRaw.forEach(supplyRow => {
        supplyData[supplyRow.zone_idx] = Number.parseFloat(supplyRow.num_stations_in_5minute_range);
    });

    // use partial application to create a tooltip processor for the scenario
    // the first selects the scenario, the second displays the data for the point
    return (scenarioName) => {

        if (!(scenarioName in allData)) {
            return (zoneIdx) => "<no data>";
        }

        const selectedScenarioData = allData[scenarioName];
        const currentScenarioTooltip = {};
        selectedScenarioData.forEach((scenarioRow) => {
            currentScenarioTooltip[scenarioRow.zone_idx] = {
                "incidentsPerDay": demandData[scenarioRow.zone_idx] / 365.0,
                "availableUnits": supplyData[scenarioRow.zone_idx],
                "accessibilityScore": Number.parseFloat(scenarioRow.accessibility_score)
            }
        });

        // return a function which can use the data we just precomputed
        return (zoneIdx) => currentScenarioTooltip[zoneIdx];
    }
}

function refreshData(mapCtx, data) {
    const facilities = drawFacilities(mapCtx, data.sfFacilityData);

    let gridValues = data.baselineFcaOutput;
    if (visType === 'sim' && simType === 'rt') {
        gridValues = data.baselineResponseTime;
    } else if (visType === 'demand') {
        gridValues = data.demandData;
    }
    const gridDrawer = setupGridDrawer(mapCtx, data.mapGridData, gridValues);
    const mapGridCells = gridDrawer(gridValues);
    const toolTipDataProcessor = createTooltipDataProcessor(
        data.baselineFcaOutput,
        data.simulationFcaOutput,
        data.demandData,
        data.supplyData);

    if (visType === 'sim') {
        setupEventHandlers(mapCtx, data, mapGridCells, gridDrawer, toolTipDataProcessor);
    }


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

    const scale = baseMap.append("g")

    const scaleOffsetY = 50
    const scaleOffsetX = 50

    scale.append("rect")
        .attr("width", "140")
        .attr("height", "2.5")
        .attr("x", (scaleOffsetX + 0) + "")
        .attr("y", (scaleOffsetY + 15) + "")
        .attr("fill", "gray")

    scale.append("rect")
        .attr("width", "2.5")
        .attr("height", "35")
        .attr("x", (scaleOffsetX + 0) + "")
        .attr("y", (scaleOffsetY + 0) + "")
        .attr("fill", "gray")

    scale.append("rect")
        .attr("width", "2.5")
        .attr("height", "35")
        .attr("x", (scaleOffsetX + 140) + "")
        .attr("y", (scaleOffsetY + 0) + "")
        .attr("fill", "gray")

    scale.append("text")
        .attr("x", (scaleOffsetX + 40) + "")
        .attr("y", (scaleOffsetY + 5) + "")
        .attr("fill", "gray")
        .text("one mile")

    baseMap.selectAll("path")
        .data(geoObj.features)
        .enter()
        .append("path")
        .attr("d", (feature) => path(feature))
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
        .attr("d", (feature) => mapCtx.path(feature))
        .attr("fill", "red")
        .attr("stroke", "red")
}

function setupGridDrawer(mapCtx, gridDefinition, initialGridValues) {

    const valMin = d3.min(initialGridValues, x => Number.parseFloat(x.value));
    const valMax = d3.max(initialGridValues, x => Number.parseFloat(x.value));
    const valMid = d3.mean(initialGridValues, x => Number.parseFloat(x.value));

    // reverse color scale for demand
    let range = ["red", "yellow", "green"]
    if (visType === 'demand') {
        range = ["green", "yellow", "red"]
    }

    const colorScale = d3.scaleLinear()
        .domain([valMin, valMid, valMax])
        .range(range);

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
                .attr("d", (feature) => mapCtx.path(feature))
                .attr("fill-opacity", "0.25")
                .attr("id", (feature) => {
                    return "zone_idx_" + feature.properties.zone_idx;
                })
                .attr("fill", (feature) => {
                    const zoneIdx = feature.properties.zone_idx + "";
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
                let currVal = valLookup[zoneIdx];
                currVal = (currVal > valMax) ? valMax : currVal;
                currVal = (currVal < valMin) ? valMin : currVal;
                d3.select("#zone_idx_" + zoneIdx)
                    .attr("fill", colorScale(currVal));
            }
        }

        return mapGridCells;
    }

    return gridDrawer;
}

function updateSimTooltips(tooltipData, simulationTooltipData) {
    if (tooltipData) {
        $("#daily_fire_incidents").text(Math.ceil(tooltipData.incidentsPerDay))
        $("#num_fire_stations").text(tooltipData.availableUnits)
        $("#num_fire_stations_vs_incidents").text((tooltipData.incidentsPerDay / tooltipData.availableUnits).toFixed(2))
        $("#accessibility_score").text(tooltipData.accessibilityScore.toFixed(6))
        if (simulationTooltipData) {
            $("#accessibility_score_sim").text(simulationTooltipData.accessibilityScore.toFixed(6))
            $("#accessibility_score_increase").text(
                "+" + (100.0 * simulationTooltipData.accessibilityScore / tooltipData.accessibilityScore - 100).toFixed(1) + "%");
        }
    } else {
        $("#daily_fire_incidents").text("-")
        $("#num_fire_stations").text("-")
        $("#num_fire_stations_vs_incidents").text("-")
        $("#accessibility_score").text("-")
        $("#accessibility_score_sim").text("-")
        $("#accessibility_score_increase").text("-")
    }
}

function setupEventHandlers(mapCtx, data, mapGridCells, gridDrawer, toolTipDataProcessor) {

    const travelTimeLookup = {};
    const originalColors = {};
    const travelTime = data.travelTime;
    let simulationData = data.simulationFcaOutput;
    if (simType === 'rt') {
        simulationData = data.simulationResponseTime;
    }

    const currentTooltipProcessor = toolTipDataProcessor("baseline");
    let simulationTooltipProcessor = null;

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

    $("#reset_fca").click(function (evt) {
        simulationTooltipProcessor = null;
        $("#accessibility_score_sim").text("-")
        $("#accessibility_score_increase").text("-")
    });


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

        // create a new tooltip processor for our scenario
        simulationTooltipProcessor = toolTipDataProcessor(simulationKey);
        // populate the tooltip
        const tooltipData = currentTooltipProcessor(zoneIdx) || false;
        const simulationTooltipData = (simulationTooltipProcessor != null) ?
            (simulationTooltipProcessor(zoneIdx) || false)
            : false;
        updateSimTooltips(tooltipData, simulationTooltipData);

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

        // populate the tooltip
        const tooltipData = currentTooltipProcessor(zoneIdx) || false;
        const simulationTooltipData = (simulationTooltipProcessor != null) ?
            (simulationTooltipProcessor(zoneIdx) || false)
            : false;
        updateSimTooltips(tooltipData, simulationTooltipData);

    }).on("mouseout", (x) => {
        let zoneIdx = x.properties.zone_idx + "";
        d3.select("#zone_idx_" + zoneIdx).attr("stroke", "none");
        resetColors();
    });
}

function drawSimulationLegend() {
    svgLegend.selectAll("*").remove();

    const fireSymbol = svgLegend
        .append("circle")
        .attr("r", "10")
        .attr("fill", "red")
        .attr("cx", "30")
        .attr("cy", "30")

    const fireLabel = svgLegend
        .append("text")
        .attr("x", "50")
        .attr("y", "35")
        .attr("style", "font-size: 14pt;")
        .text("Existing fire station")

    const simSymbol = svgLegend
        .append("circle")
        .attr("r", "10")
        .attr("fill", "blue")
        .attr("cx", "300")
        .attr("cy", "30")

    const simLabel = svgLegend
        .append("text")
        .attr("x", "325")
        .attr("y", "35")
        .attr("style", "font-size: 14pt;")
        .text("New fire station (simulated point)")

    const simAreaSymbol = svgLegend
        .append("rect")
        .attr("width", "20")
        .attr("height", "20")
        .attr("fill", "rgb(196, 141, 221)")
        .attr("x", "290")
        .attr("y", "60")

    const simAreaLabel = svgLegend
        .append("text")
        .attr("x", "325")
        .attr("y", "70")
        .attr("style", "font-size: 14pt;")
        .text("New fire station coverage area")

    const simAreaLabel2 = svgLegend
        .append("text")
        .attr("x", "325")
        .attr("y", "90")
        .attr("style", "font-size: 12pt;")
        .text("(<= 5 minute travel time)")

    const spatialYOffset = 130;
    let colorLegendLabel = simType === 'rt' ? "Response Time:" : "Spatial Accessibility (2SFCA):";
    let colorLegendHighLabel = simType === 'rt' ? "Fast expected response to a new incident" : "High # of available fire units per incident";
    let colorLegendMedLabel = simType === 'rt' ? "Moderate expected response to a new incident" : "Avg # of available fire units per incident";
    let colorLegendLowLabel = simType === 'rt' ? "Slower expected response to a new incident" : "Low # of available fire units per incident";

    const spatialLabel = svgLegend
        .append("text")
        .attr("x", "20")
        .attr("y", spatialYOffset + "")
        .text(colorLegendLabel)
        .attr("style", "font-size: 14pt; font-weight: bold;")

    const colorLegendHigh = svgLegend
        .append("rect")
        .attr("width", "20")
        .attr("height", "20")
        .attr("x", "40")
        .attr("y", (spatialYOffset + 15) + "")
        .attr("fill", "rgb(44,150,0)")

    const highLabel = svgLegend
        .append("text")
        .attr("x", "70")
        .attr("y", (spatialYOffset + 30) + "")
        .attr("style", "font-size: 12pt;")
        .text(colorLegendHighLabel)

    const colorLegendMid = svgLegend
        .append("rect")
        .attr("width", "20")
        .attr("height", "20")
        .attr("x", "40")
        .attr("y", (spatialYOffset + 50) + "")
        .attr("fill", "rgb(239,230,100)")

    const midLabel = svgLegend
        .append("text")
        .attr("x", "70")
        .attr("y", (spatialYOffset + 65) + "")
        .attr("style", "font-size: 12pt;")
        .text(colorLegendMedLabel)

    const colorLegendLow = svgLegend
        .append("rect")
        .attr("width", "20")
        .attr("height", "20")
        .attr("x", "40")
        .attr("y", (spatialYOffset + 85) + "")
        .attr("fill", "rgb(239,107,100)")

    const lowLabel = svgLegend
        .append("text")
        .attr("x", "70")
        .attr("y", (spatialYOffset + 100) + "")
        .attr("style", "font-size: 12pt;")
        .text(colorLegendLowLabel)
}