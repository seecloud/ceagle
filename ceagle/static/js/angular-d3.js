/* Angular directive for D3 line chart.

  Sample of usage:

  <d3-line-chart
      title="Chart title"
      scope_var="scope_data.line_chart_data">
  </d3-line-chart>

  * title     - Chart title
  * scope - Variable in controller scope that contains chart data

    Data format is very simple
    [["Date in format '%d-%b-%yT%H'", float_value], [...], ...]
*/

angular.module('d3.line_chart', []);
angular.module('d3.line_chart')
  .directive('d3LineChart', function() {
    return {
      restrict: 'EA',
      transclude: true,
      scope: false,
      link: function(scope, iElement, iAttrs) {

        var svg = d3.select(iElement[0])
          .append("svg")
            .attr("width", "100%")
            .attr("height", "100%");

        var _render_func = line_chart(svg, iAttrs["title"]);

        scope.$watch(iAttrs["scope"], function(newVals, oldVals) {
          return _render_func(newVals);
        }, true);
      }
    }
  });


var line_chart = function(svg, title){
    var margin = {top: 15, right: 20, bottom: 20, left: 35}
    var parse_date = d3.timeParse("%Y-%m-%dT%H:%M");

    svg.attr("class", "line_chart")

    var g = svg.append("g");
    g.append("text")
      .text(title)
      .attr("class", "title")
      .attr("x", 5)
      .attr("y", -5);

    var x_axis = g.append("g").attr("class", "x axis");
    var y_axis = g.append("g").attr("class", "y axis");

    var path = g.append("path").attr("class", "line")

    var render = function(data){
        bounding_rect = svg.node().getBoundingClientRect();

        width = bounding_rect["width"] - margin.left - margin.right,
        height = bounding_rect["height"] - margin.top - margin.bottom;

        var x = d3.scaleTime().range([0, width]);
        var y = d3.scaleLinear().range([height, 0]);

        x.domain(d3.extent(data, function(d) { return parse_date(d[0]); }));
        y.domain(d3.extent(data, function(d) { return d[1] }));

        svg
          .attr("width", width + margin.left + margin.right)
          .attr("height", height + margin.top + margin.bottom)

        g
          .attr("transform",
                 "translate(" + margin.left + "," + margin.top + ")");

        var xAxis = d3.axisBottom()
          .ticks(2)
          .scale(x);

        var yAxis = d3.axisLeft()
          .tickValues(y.domain())
          .scale(y);

        x_axis
          .attr("transform", "translate(0," + height + ")")
          .call(xAxis);

        y_axis.call(yAxis);

        var line = d3.line()
          .x(function(d) { return x(parse_date(d[0])); })
          .y(function(d) { return y(d[1]); })
          .defined(function(d) { return d[1] != null; })

        path.datum(data).transition().attr("d", line);
    }

    return render;
}
