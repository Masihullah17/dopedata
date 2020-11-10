var data = [{
    'name':"Jan",'value': 7
  },{
    'name':"Feb",'value': 19
  },{
    'name':"Mar",'value': 12
  },{
    'name':"Apr",'value': 14
  },{
    'name':"May", 'value': 23
  },{
    'name':"Jun",'value': 8
  },{
    'name':"Jul",'value': 11
  },{
    'name':"Aug",'value': 14
  },{
    'name':"Sep",'value': 11
  },{
    'name':"Oct",'value': 10
  },{
    'name':"Nov",'value': 8
  },{
    'name':"Dec",'value': 9
  },];
  
  
  // Set the dimensions of our chart to be displayed 
  var barsWidth = 180,
      barsHeight = 90,
      axisMargin = 30;
  
  var chartHeight = barsHeight+axisMargin,
      chartWidth = barsWidth+axisMargin;
  
  
  // Select the chart element on the page so we can reference it in code
  // Also set the width and height attributes of the chart SVG 
  var chart = d3.select('#chart_4').append("svg")
      .attr('width', chartWidth+100)
      .attr('height', chartHeight);
  
  // Create a linear scale for our y-axis to map datapoint values to pixel heights of bars
  var yScale = d3.scaleLinear()
      .domain([0,d3.max(data, function(d){
      // return the value property of each datapoint so the max function can compare
          return d.value;
      })])
      .rangeRound([barsHeight, 0]);
  
  // Create a scale that returns the bands each bar should be in along the x-axis
  let xScale = d3.scaleBand()
      .domain(
          data.map(
              function(d){
          // For each datapoint in our data array
          // Return the name property into our new domain array
                  return d.name;
              }
          )
      )
      .rangeRound([0,barsWidth])
      .padding(0.1);
  
  // Create an SVG group that we will add the individual bar elements of our chart to
  var bars = chart.append('g')
      .attr('id', "bars-container");
  
  // Bind the data to our .bars svg elements
  // Create a rectangle for each data point and set position and dimensions using scales
  bars.selectAll('.bar')
      .data(data)
      .enter().append("rect")
          .attr('class', "bar")
          .attr('x', function(d){
              return xScale(d.name);
          })
          .attr('y', function(d){
              return yScale(d.value); 
          })
          .attr('width', xScale.bandwidth())
          .attr('height', function(d){return barsHeight-yScale(d.value);});
  
  // Move the bars so that there is space on the left for the y-axis
  bars.attr('transform', 'translate('+axisMargin+',0)');
  
  // Create a new SVG group for the y-axis elements
  // Generate the y-axis with 10 ticks and move into position
  yAxis = chart.append('g')
      .attr('id','y-axis')
      .call(d3.axisLeft(yScale).ticks(10))
          .attr('transform', 'translate('+axisMargin+',0)');
  
  // Create another group for the x-axis elements
  // Generate the x-axis using the our x scale and move into positon
  // Select the text elements and rotate by 45 degrees
  xAxis = chart.append('g')
      .attr('id', 'x-axis')
      .call(d3.axisBottom(xScale))
      .attr('transform', 'translate('+axisMargin+','+barsHeight+')')
      .selectAll("text")
          .style("text-anchor",'start')
          .attr('transform', 'rotate(45)');
  
          
  