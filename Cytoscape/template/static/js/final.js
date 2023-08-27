var cy = cytoscape({
  container: document.getElementById("cy"), // container to render in, declared in HTML

  wheelSensitivity: 0.1,

  style: [
    // the stylesheet for the graph
    {
      selector: "node",
      style: {
        "background-color": "#666",
        "label": "data(label)",
        "shape": "rectangle",
        "font-size": 10,
        "text-background-opacity": 1,
        "text-background-shape": "rectangle",
        "text-background-color": "black",
        "color": "white",
        "text-valign": "bottom"
      },
    },
    {
      selector: "edge",
      style: {
        "width": 3,
        "line-color": "#aaa",
        "curve-style": "bezier",
        "control-point-step-size": 80, // change this value to adjust the curve
        "line-style": "dashed",
        "line-dash-pattern": [6, 4],
        "font-size": 10,
        "text-wrap": "wrap",
        "text-max-width": "100px",
        "source-text-offset": "50px",
        "target-text-offset": "10px",
        "source-text-margin-y": "-10px",
        "target-text-margin-y": "-10px",
        "text-opacity": 0,
        "text-background-opacity": 1,
        "text-background-color": "black",
        "color": "yellow",
      },
    },
  ],
});

vlan.forEach(VLAN => {
  cy.add({
    data: { id: VLAN.id, label: VLAN.id },
    style: {
      "background-image": "./images/pc.png",
      "background-fit": "contain",
      "background-opacity": "0",
    }
  })
});

cy.add([{ data: router[0].data }]);

for (let i = 0; i < coreDevice.length; i++) {
  cy.add({
    data: coreDevice[i].data
  });
};

for (let i = 0; i < distDevice.length; i++) {
  cy.add({
    data: distDevice[i].data
  });
};

for (let i = 0; i < accessDevice.length; i++) {
  cy.add({
    data: accessDevice[i].data
  });
};

for (let i = 0; i < portDevice.length; i++) {
  cy.add(
    {
      data: portDevice[i].data, style: portDevice[i].style
    },
  );
};

var edge = cy.getElementById('router-coreSwt0');

edge.style('sourceLabel', 'Gi0/0/1');

edge.style("line-style", "solid");

cy.nodes('[layer="core"]').style({
  "background-image": "./images/3650.png",
  "background-fit": "contain",
  "background-opacity": "0",
});

cy.nodes('[layer="distribution"]').style({
  "background-image": "./images/3650.png",
  "background-fit": "contain",
  "background-opacity": "0",
});

cy.nodes('[layer="access"]').style({
  "background-image": "./images/sw.png",
  "background-fit": "contain",
  "background-opacity": "0",
});

cy.nodes('[id="router"]').style({
  "background-image": "./images/router.png",
  "background-fit": "contain",
  "background-opacity": "0",
});

cy.on("select unselect", "edge", function (evt) {
  evt.target.style("text-opacity", evt.target.selected() ? 1 : 0);
  evt.target.style("line-color", evt.target.selected() ? "red" : "#aaa");
  evt.target.style("z-index", evt.target.selected() ? "3" : "1");
});

cy.on("tap", function (event) {
  if (event.target === cy) {
    cy.elements().style("line-color", "#aaa"); // reset line color of all edges
    cy.elements().style("z-index", "1");
  }
});

cy.nodes().on("tap", function (event) {
  var clickedNode = event.target;
  var connectedEdges = cy.elements().edgesWith(clickedNode);

  cy.elements().style("line-color", "#aaa"); // reset line color of all edges
  setTimeout(function () {
    connectedEdges.style("line-color", "black"); // highlight the edges connected to the clicked node
    connectedEdges.style("z-index", "3");
  }, 50);
});

var layout = cy.layout({
  name: "dagre",
  rankDir: "TB", // top to bottom
  rankSep: 150,
  nodeSep: 150,
});

layout.run();



