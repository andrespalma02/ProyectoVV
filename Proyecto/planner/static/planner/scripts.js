var treeData = anychart.data.tree(data, "as-tree");
var chart = anychart.ganttProject();
chart.data(treeData);
chart.getTimeline().scale().maximum(Date.UTC(2018, 6, 30));
chart.container("container");
chart.draw();
