var data = [
  {name: "Category A", value: 5},
  {name: "Category B", value: 20},
  {name: "Category C", value: 50},
  {name: "Category D", value: 10},
  {name: "Category E", value: 10},
  {name: "Category F", value: 5}
];
  var text = "";
  
  var width = 105;
  var height = 105;
  var thickness = 15;
  var duration = 75;
  
  var radius = Math.min(width, height) / 2;
  var color = d3.scaleOrdinal()
     .range(["#d0ccd0", "#d6d0db", "#605856", "#1c6e8c", "#274156", "skyblue"]); ;
  
  var svg_7 = d3.select("#chart_2")
  .append('svg')
  .attr('class', 'pie')
  .attr('width', width)
  .attr('height', height);
  
  var g = svg_7.append('g')
  .attr('transform', 'translate(' + (width/2) + ',' + (height/2) + ')');
  
  var arc = d3.arc()
  .innerRadius(radius - thickness)
  .outerRadius(radius);
  
  var pie = d3.pie()
  .value(function(d) { return d.value; })
  .sort(null);
  
  var path = g.selectAll('path')
  .data(pie(data))
  .enter()
  .append("g")
  .on("mouseover", function(d) {
        let g = d3.select(this)
          .style("cursor", "pointer")
          .style("fill", "black")
          .append("g")
          .attr("class", "text-group");
   
        g.append("text")
          .attr("class", "name-text")
          .text(`${d.data.name}`)
          .attr('text-anchor', 'middle')
          .attr('dy', '-1.2em');
    
        g.append("text")
          .attr("class", "value-text")
          .text(`${d.data.value}`)
          .attr('text-anchor', 'middle')
          .attr('dy', '.6em');
      })
    .on("mouseout", function(d) {
        d3.select(this)
          .style("cursor", "none")  
          .style("fill", color(this._current))
          .select(".text-group").remove();
      })
    .append('path')
    .attr('d', arc)
    .attr('fill', (d,i) => color(i))
    .on("mouseover", function(d) {
        d3.select(this)     
          .style("cursor", "pointer")

      })
    .on("mouseout", function(d) {
        d3.select(this)
          .style("cursor", "none")
          

      })
    .each(function(d, i) { this._current = i; });
  
  
  g.append('text')
    .attr('text-anchor', 'middle')
    .attr('dy', '.35em')
    .text(text);