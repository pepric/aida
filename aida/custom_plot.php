<div id="plot_settings" style="display:none; padding: 0">
  <section class="panel panel-featured panel-featured-primary cp-panel">
    <header class="panel-heading">
      <div class="cpanel-actions">
        <a href="#" class="fa fa-times" onclick="hide_custom_plot()"></a>
      </div>

      <h2 class="panel-title">Plot Customization</h2>
    </header>                      
    <div class="panel-body"> 
      <div class="panel-group" id="accordion2">
	  
		<!-- GENERAL PANEL -->
        <div class="panel panel-accordion panel-accordion-primary">
          <div class="panel-heading">
            <h4 class="panel-title">
              <a class="accordion-toggle collapsed" data-toggle="collapse" data-parent="#accordion2" href="#collapse2One" aria-expanded="false">General</a>
			  
            </h4>
          </div>
          <div id="collapse2One" class="accordion-body collapse" aria-expanded="false" style="height: 0px;">
            <div class="panel-body">
				<div class="group__heading">
					<span class="cp-grp-head">Background</span>
					<span class="cp-toggle-btn"><button type="button" class="mb-xs mt-xs mr-xs btn btn-xs btn-primary" onclick="toggle('cp-gen-bg')">Toggle</button>
					</span>
				</div>
			  <div id="cp-gen-bg">
				  <div class="field">
					<div class="field-title">Plot Background</div>
					<div class="field-widget">
						  <div class="input-group color colorpicker-element" data-color="#ffffff" data-color-format="hex" data-plugin-colorpicker="">
							<input id="img-color-bg" type="color" class="input-group-addon color-pick" value="#ffffff" colorpick-eyedropper-active="false" data-change="bg">
							<input id="color-bg" type="text" class="form-control" value="#ffffff" oninput="change_color_from_text(this)" data-change="bg">
						  </div> 				
					</div>                              
				  </div>
				  <div class="field">
					<div class="field-title">Margin Color</div>
					<div class="field-widget">
						  <div class="input-group color colorpicker-element" data-color="#ffffff" data-color-format="hex" data-plugin-colorpicker="">
							<input id="img-color-margins" type="color" class="input-group-addon color-pick" value="#ffffff" colorpick-eyedropper-active="false" data-change="margins">
							<input id="color-margins" type="text" class="form-control" value="#ffffff" oninput="change_color_from_text(this)" data-change="margins">
						  </div> 				
					</div>                              
				  </div>
              </div>

				<div class="group__heading">
					<span class="cp-grp-head">Text</span>
					<span class="cp-toggle-btn"><button type="button" class="mb-xs mt-xs mr-xs btn btn-xs btn-primary" onclick="toggle('cp-gen-text')">Toggle</button>
					</span>
				</div>              
				<div id="cp-gen-text">
				  <div class="field">
					<div class="field-title">Typeface</div>
					<div class="field-widget">
					  <select name="typeface" id="tf_general" class="" onchange="set_font(this.value, 'all', 'family')">
						<option value="" disabled selected>Select an option</option>
						<option value="Arial" style="font-family:Arial">Arial</option>
						<option value="Courier New" style="font-family:'Courier New'">Courier New</option>
						<option value="Open Sans" style="font-family:'Open Sans'">Open Sans</option>
						<option value="Times New Roman" style="font-family:'Times New Roman'">Times New Roman</option>                      
					  </select>
					</div>                              
				  </div>
				  <div class="field">
					<div class="field-title">Font Size</div>
					<div class="field-widget"><input type="number" value="17" onchange="set_font(this.value, 'all', 'size')"></div>                              
				  </div>                              
				  <div class="field">
					<div class="field-title">Font Color</div>
					<div class="field-widget">
					  <div class="input-group color colorpicker-element" data-color="#000000" data-color-format="hex" data-plugin-colorpicker="">
						<input id="img-color-all" type="color" class="input-group-addon color-pick" value="#000000" colorpick-eyedropper-active="false" data-change="" data-elem="font">
						<input id="color-all" type="text" class="form-control" value="#000000" oninput="change_color_from_text(this)" data-change="" data-elem="font">				
					  </div>  
					</div>                              
				  </div> 
				</div>
				<div class="group__heading">
					<span class="cp-grp-head">Title</span>
					<span class="cp-toggle-btn"><button type="button" class="mb-xs mt-xs mr-xs btn btn-xs btn-primary" onclick="toggle('cp-gen-title')">Toggle</button>
					</span>
				</div> 				
				<div id="cp-gen-title">             
				  <div class="field">
					<div class="field-title">Text (HTML)</div>
					<div class="field-widget"><textarea value="" oninput="set_text(this.value, 'title')"></textarea></div>                              
				  </div>                          
				  <div class="field">
					<div class="field-title">Typeface</div>
					<div class="field-widget">
					  <select name="typeface" id="tf_general" class="" onchange="set_font(this.value, 'title', 'family')">
						<option value="" disabled selected>Select an option</option>
						<option value="Arial" style="font-family:Arial">Arial</option>
						<option value="Courier New" style="font-family:'Courier New'">Courier New</option>
						<option value="Open Sans" style="font-family:'Open Sans'">Open Sans</option>
						<option value="Times New Roman" style="font-family:'Times New Roman'">Times New Roman</option>                      
					  </select>
					</div>                              
				  </div>
				  <div class="field">
					<div class="field-title">Font Size</div>
					<div class="field-widget"><input type="number" value="17" onchange="set_font(this.value, 'title', 'size')"></div>                              
				  </div>
				  <div class="field">
					<div class="field-title">Font Color</div>
					  <div class="input-group color colorpicker-element" data-color="#000000" data-color-format="hex" data-plugin-colorpicker="">
						<input id="img-color-title" type="color" class="input-group-addon color-pick" value="#000000" colorpick-eyedropper-active="false" data-change="" data-elem="font">
						<input id="color-title" type="text" class="form-control" value="#000000" oninput="change_color_from_text(this)" data-change="" data-elem="font">				
					  </div>                              
				  </div>
				  <div class="field">
					<div class="field-title">Horizontal Position</div>
					<div class="field-widget">
								<div class="slidecontainer">
								  <input id="listenSlider2" class="slider-txt" type="text" value="50" />							
								  <input type="range" min="1" max="100" value="50" class="slider" id="hslider">
								</div>	
					</div>                              
				  </div>
				</div>
            </div>
          </div>
        </div>
        <!-- TRACES PANEL -->
		<div class="panel panel-accordion panel-accordion-primary">
          <div class="panel-heading">
            <h4 class="panel-title">
              <a class="accordion-toggle collapsed" data-toggle="collapse" data-parent="#accordion2" href="#collapse2Two" aria-expanded="false">Traces</a>
            </h4>
          </div>
          <div id="collapse2Two" class="accordion-body collapse" aria-expanded="false" style="height: 0px;">
            <div class="panel-body">
				<div class="field"><select name="tracelist" id="tracelist" class="" onchange="build_trace_form(this.value)"></select></div>
				<div id="trace_set" style="display:none">
					<div class="field" id="trace_name">
						<div class="field-title">Name</div>
						<div class="field-widget">
							<input id="tr-input-name" type="text" class="form-control" value="">
						</div>                              
					</div>

					<div id="cp-tr-display" style="display:none">
						<div class="field">
							<div class="field-title">Display</div>
							<div class="field-widget">
								<div class="btn-group btn-group-toggle">
									<label class="">
											<input type="checkbox" name="tr_points_show" id="tr-p" onchange="display_plot_elem('markers', this.id)"> Points
									</label>
									<label class="">
											<input type="checkbox" name="tr_lines_show" id="tr-l" onchange="display_plot_elem('lines', this.id)"> Lines
									</label>
									<label class="">
											<input type="checkbox" name="tr_text_show" id="tr-t" onchange="display_plot_elem('text', this.id)"> Text
									</label>									
								</div>                
							</div>                              
						</div>						
					</div>

					<div id="cp-tr-markers" style="display:none">
						<div class="group__heading">
							<span class="cp-grp-head">Points</span>
							<span class="cp-toggle-btn"><button type="button" class="mb-xs mt-xs mr-xs btn btn-xs btn-primary" onclick="toggle('cp-tr-markstyle')">Toggle</button>
							</span>
						</div>              
						<div id="cp-tr-markstyle">
							<div class="field">
								<div class="field-title">Color</div>
								<div class="field-widget">
								  <div class="input-group color colorpicker-element" data-color="#000000" data-color-format="hex" data-plugin-colorpicker="">
									<input id="img-color-markers" type="color" class="input-group-addon color-pick" value="#000000" colorpick-eyedropper-active="false" data-change="tr-markers" data-elem="">
									<input id="color-markers" type="text" class="form-control" value="#000000" oninput="change_color_from_text(this)" data-change="tr-markers" data-elem="">				
								  </div>   
								</div>                             
							</div> 
						</div>
					</div>

					<div id="cp-tr-lines" style="display:none">
							LINES
					</div>

					<div id="cp-tr-text" style="display:none">
							TEXT ----- TODO
					</div>					
				</div>
            </div>
          </div>
        </div>
        <!-- AXES PANEL -->
		<div class="panel panel-accordion panel-accordion-primary">
          <div class="panel-heading">
            <h4 class="panel-title">
              <a class="accordion-toggle collapsed" data-toggle="collapse" data-parent="#accordion2" href="#collapse2Three" aria-expanded="false">Axes</a>
            </h4>
          </div>
          <div id="collapse2Three" class="accordion-body collapse" aria-expanded="false" style="height: 0px;">
            <div class="panel-body">
				  <div class="btn-group btn-group-toggle btn-group-justified" data-toggle="buttons">
					<label class="btn btn-default active">
					  <input type="radio" name="axis_sel" id="alla" autocomplete="off" value="all" checked> ALL
					</label>
					<label class="btn btn-default">
					  <input type="radio" name="axis_sel" id="xa" value="x" autocomplete="off"> X
					</label>
					<label class="btn btn-default">
					  <input type="radio" name="axis_sel" id="ya" value="y" autocomplete="off"> Y
					</label>
				  </div>            
			  
			  
				<div class="group__heading">
					<span class="cp-grp-head">Titles</span>
					<span class="cp-toggle-btn"><button type="button" class="mb-xs mt-xs mr-xs btn btn-xs btn-primary" onclick="toggle('cp-ax-titles')">Toggle</button>
					</span>
				</div> 			  
				<div id="cp-ax-titles">
				  <div class="field" id="axis-title-text" style="display:none">
					<div class="field-title">Text (HTML)</div>
					<div class="field-widget">
						<textarea value="" oninput="set_text(this.value, 'axes')"></textarea>
					</div>                              
				  </div>               
				  <div class="field">
					<div class="field-title">Typeface</div>
					<div class="field-widget">
					  <select name="typeface" id="tf_axis" class="" onchange="set_font(this.value, 'axis', 'family', 'titles')">
						<option value="" disabled selected>Select an option</option>
						<option value="Arial" style="font-family:Arial">Arial</option>
						<option value="Courier New" style="font-family:'Courier New'">Courier New</option>
						<option value="Open Sans" style="font-family:'Open Sans'">Open Sans</option>
						<option value="Times New Roman" style="font-family:'Times New Roman'">Times New Roman</option>                      
					  </select>                
					</div>                              
				  </div>
				  <div class="field">
					<div class="field-title">Font Size</div>
					<div class="field-widget"><input id="font-axis-title" type="number" value="12" onchange="set_font(this.value, 'axis', 'size', 'titles')"></div>                              
				  </div>                              
				  <div class="field">
					<div class="field-title">Font Color</div>
						  <div class="input-group color colorpicker-element" data-color="#000000" data-color-format="hex" data-plugin-colorpicker="">
							<input id="img-tcolor-axis" type="color" class="input-group-addon color-pick" value="#000000" colorpick-eyedropper-active="false" data-change="titles" data-elem="font">
							<input id="tcolor-axis" type="text" class="form-control" value="#000000" oninput="change_color_from_text(this)" data-change="titles" data-elem="font">
						  </div>                              
				  </div> 
				</div> 

				<div id="range_div" style="display:none">
					<div class="group__heading">
						<span class="cp-grp-head">Range</span>
						<span class="cp-toggle-btn"><button type="button" class="mb-xs mt-xs mr-xs btn btn-xs btn-primary" onclick="toggle('cp-ax-range')">Toggle</button>
						</span>
					</div>
					<div id="cp-ax-range">					
					  <div class="field">
						<div class="field-title">Type</div>
						<div class="field-widget">
						  <select name="range_type" id="rangetype" onchange="set_rangetype(this.value)">
							<option value="date">Date</option>
							<option value="linear">Linear</option>
							<option value="log">Log</option>
						
						  </select> 					
						</div>                              
					  </div>               
					  <div class="field">
						<div class="field-title">Range</div>
						<div class="field-widget">
						  <div class="btn-group btn-group-toggle">
							<label class="">
							  <input type="radio" name="range_sel" id="autor" value="auto" checked> Auto
							</label>
							<label class="">
							  <input type="radio" name="range_sel" id="customr" value="custom" > Custom
							</label>
						  </div>                
						</div>                              
					  </div>
					  <div id="range_lim" style="display:none">
						<div class="field">
						  <div class="field-title">Min</div>
						  <div class="field-widget" id="minrangelim">content</div>                              
						</div>                              
						<div class="field">
						  <div class="field-title">Max</div>
						  <div class="field-widget" id="maxrangelim">content</div>                              
						</div>
					  </div>
					</div>
				</div>				  
			  
				<div class="group__heading">
					<span class="cp-grp-head">Lines</span>
					<span class="cp-toggle-btn"><button type="button" class="mb-xs mt-xs mr-xs btn btn-xs btn-primary" onclick="toggle('cp-ax-lines')">Toggle</button>
					</span>
				</div> 			  
				<div id="cp-ax-lines">			  
            
				  <div class="field">
					<div class="field-title">Axis Line</div>
					<div class="field-widget">
					  <div class="btn-group btn-group-toggle">
						<label class="">
						  <input type="radio" name="axis_show" id="axiss" value="show"> Show
						</label>
						<label class="">
						  <input type="radio" name="axis_show" id="axish" value="hide"  checked> Hide
						</label>
					  </div>                
					</div>                              
				  </div>
				  <div id="axis_show_line" style="display:none">
					<div class="field">
					  <div class="field-title">Axis Thickness</div>
					  <div class="field-widget"><input id="axis-thick" type="number" value="1" min="1" onchange="set_thickness(this.value, 'axis')"></div>                              
					</div>                              
					<div class="field">
						<div class="field-title">Axis Color</div>
						<div class="field-widget">					  
							<div class="input-group color colorpicker-element" data-color="#444444" data-color-format="hex" data-plugin-colorpicker="">
							<input id="img-color-axis" type="color" class="input-group-addon color-pick" value="#444444" style="background-color:#444444" colorpick-eyedropper-active="false" data-change="axisline">
							<input id="color-axis" type="text" class="form-control" value="#444444" oninput="change_color_from_text(this)" data-change="axisline">
						  </div>
						</div>                              
					</div>
				  </div>
				  <div class="field">
					<div class="field-title">Grid Lines</div>
					<div class="field-widget">
					  <div class="btn-group btn-group-toggle">
						<label class="">
						  <input type="radio" name="grid_show" id="grids" value="show" checked> Show
						</label>
						<label class="">
						  <input type="radio" name="grid_show" id="gridh" value="hide"> Hide
						</label>
					  </div>                
					</div>                              
				  </div>
				  
				  <div id="grid_show_line">
					<div class="field">
					  <div class="field-title">Grid Thickness</div>
					  <div class="field-widget"><input id="grid-thick" type="number" value="1" min="1" onchange="set_thickness(this.value, 'grid')"></div>                              
					</div>                              
					<div class="field">
					  <div class="field-title">Grid Color</div>
					  <div class="field-widget">
						  <div class="input-group color colorpicker-element" data-color="#EBF0F8" data-color-format="hex" data-plugin-colorpicker="">
							<input id="img-color-grid" type="color" class="input-group-addon color-pick" value="#EBF0F8" style="background-color:#ebf0f8" colorpick-eyedropper-active="false" data-change="grid">
							<input id="color-grid" type="text" class="form-control" value="#EBF0F8" oninput="change_color_from_text(this)" data-change="grid">
						  </div>				  
					  
					  </div>                              
					</div>
					<div id="grspace_div" style="display:none">				
						<div class="field">
						  <div class="field-title">Grid Spacing</div>
						  <div class="field-widget">
							<div class="btn-group btn-group-toggle">
							  <label class="">
								<input type="radio" name="grid_spacing" id="autog" value="auto" checked> Auto
							  </label>
							  <label class="">
								<input type="radio" name="grid_spacing" id="customg" value="custom" > Custom
							  </label>
							</div>                                  
						  </div>
						</div> 
						<div id="grid_sp" style="display:none">
						  <div class="field" id="stepoff_div">
							<div class="field-title">Step Offset</div>
							<div class="field-widget" id="stepoff">content</div>                              
						  </div>                              
						  <div class="field">
							<div class="field-title">Step Size</div>
							<div class="field-widget" id="stepsize">content</div>                              
						  </div>
						</div>
					  </div>
				  </div>
				  
				  <div class="field" id="zero_line_set">
					<div class="field-title">Zero Line</div>
					<div class="field-widget">
					  <div class="btn-group btn-group-toggle">
						<label class="">
						  <input type="radio" name="zerol_show" id="zeros" value="show" checked> Show
						</label>
						<label class="">
						  <input type="radio" name="zerol_show" id="zeroh" value="hide" > Hide
						</label>
					  </div>                
					</div>                              
				  </div>
				  <div id="zero_line_show">
					<div class="field">
					  <div class="field-title">Line Thickness</div>
					  <div class="field-widget"><input id="zerol-thick" type="number" value="1" min="1" onchange="set_thickness(this.value, 'zerol')">
					  </div>                              
					</div>                              
					<div class="field">
					  <div class="field-title">Line Color</div>
					  <div class="field-widget">
						  <div class="input-group color colorpicker-element" data-color="#000000" data-color-format="hex" data-plugin-colorpicker="">
							<input id="img-color-zerol" type="color" class="input-group-addon color-pick" value="#000000" style="background-color:#000000" colorpick-eyedropper-active="false" data-change="zerol">
							<input id="color-zerol" type="text" class="form-control" value="#000000" oninput="change_color_from_text(this)" data-change="zerol">
						  </div>				  
					  </div>                              
					</div>
				  </div>              
				</div>              
				<div class="group__heading">
					<span class="cp-grp-head">Tick Labels</span>
					<span class="cp-toggle-btn"><button type="button" class="mb-xs mt-xs mr-xs btn btn-xs btn-primary" onclick="toggle('cp-ax-ticks')">Toggle</button>
					</span>
				</div>
				<div id="cp-ax-ticks">
				  <div class="field">
					<div class="field-title">Show/Hide</div>
					<div class="field-widget">
					  <div class="btn-group btn-group-toggle">
						<label class="">
						  <input type="radio" name="tickl_show" id="ticks" value="show" checked> Show
						</label>
						<label class="">
						  <input type="radio" name="tickl_show" id="tickh" value="hide"> Hide
						</label>
					  </div>                
					</div>                              
				  </div>
				  <div id="ticklabels_show">
					<div class="field" id="ticks-position" style="display:none">
					  <div class="field-title">Position</div>
					  <div class="field-widget">
						<div class="btn-group btn-group-toggle">
						  <label for="tickps" class="">
							<input type="radio" name="tickpos_show" id="tickps" value="top" ><span id="tickps_txt"> Top</span>
						  </label>
						  <label for="tickph" class="">
							<input type="radio" name="tickpos_show" id="tickph" value="bottom" checked><span id="tickph_txt"> Bottom</span>
						  </label>
						</div>                
					  </div>                              
					</div>

					<div class="field">
					  <div class="field-title">Typeface</div>
					  <div class="field-widget">
						<select name="typeface" id="tf_ticks" class="" onchange="set_font(this.value, 'axis', 'family', 'ticks')">
						  <option value="" disabled selected>Select an option</option>
						  <option value="Arial" style="font-family:Arial">Arial</option>
						  <option value="Courier New" style="font-family:'Courier New'">Courier New</option>
						  <option value="Open Sans" style="font-family:'Open Sans'">Open Sans</option>
						  <option value="Times New Roman" style="font-family:'Times New Roman'">Times New Roman</option>                      
						</select>                  
					  </div>                              
					</div>
					<div class="field">
					  <div class="field-title">Font Size</div>
					  <div class="field-widget"><input id="font-axis-ticks" type="number" value="12" onchange="set_font(this.value, 'axis', 'size', 'ticks')"></div>                              
					</div>                              
					<div class="field">
					  <div class="field-title">Font Color</div>
						  <div class="input-group color colorpicker-element" data-color="#000000" data-color-format="hex" data-plugin-colorpicker="">
							<input id="img-color-ticks" type="color" class="input-group-addon color-pick" value="#000000" colorpick-eyedropper-active="false" data-change="ticks" data-elem="font">
							<input id="color-ticks" type="text" class="form-control" value="#000000" oninput="change_color_from_text(this)" data-change="ticks" data-elem="font">
						  </div>                              
					</div>                 
					<div class="field" id="ticks-angle" style="display:none">
					  <div class="field-title">Angle</div>
					  <div class="field-widget"><input id="tick-angle" type="number" value="0" min="-180" max="180" step="1" onchange="set_angle(this.value)"></div>                              
					</div> 

				  </div>
				</div>

            </div>                 
          </div>
        </div>
		<!-- LEGEND PANEL -->
        <div class="panel panel-accordion panel-accordion-primary">
          <div class="panel-heading">
            <h4 class="panel-title">
              <a class="accordion-toggle collapsed" data-toggle="collapse" data-parent="#accordion2" href="#collapse2Four" aria-expanded="false">Legend</a>
            </h4>
          </div>
          <div id="collapse2Four" class="accordion-body collapse" aria-expanded="false" style="height: 0px;">
            <div class="panel-body">
              
              <div class="btn-group btn-group-toggle btn-group-justified" data-toggle="buttons">
                <label class="btn btn-default active">
                  <input type="radio" name="legend_sel" id="legshow" autocomplete="off" value="show"> Show
                </label>
                <label class="btn btn-default">
                  <input type="radio" name="legend_sel" id="leghide" value="hide" autocomplete="off"> Hide
                </label>
              </div>               

              <div id="leg_show">
				<div class="group__heading">
					<span class="cp-grp-head">Title</span>
					<span class="cp-toggle-btn"><button type="button" class="mb-xs mt-xs mr-xs btn btn-xs btn-primary" onclick="toggle('cp-leg-title')">Toggle</button>
					</span>
				</div> 				  
				<div id="cp-leg-title">
					<div class="field">
					  <div class="field-title">Text (HTML)</div>
					  <div class="field-widget"><textarea value="" oninput="set_text(this.value, 'legend')"></textarea></div>                              
					</div>
					<div class="field">
					  <div class="field-title">Typeface</div>
					  <div class="field-widget">
						<select name="typeface" id="tf_lg_title" class="" onchange="set_font(this.value, 'legend', 'family', 'title')">
						  <option value="" disabled selected>Select an option</option>
						  <option value="Arial" style="font-family:Arial">Arial</option>
						  <option value="Courier New" style="font-family:'Courier New'">Courier New</option>
						  <option value="Open Sans" style="font-family:'Open Sans'">Open Sans</option>
						  <option value="Times New Roman" style="font-family:'Times New Roman'">Times New Roman</option>                      
						</select>                  
					  </div>                              
					</div>
					<div class="field">
					  <div class="field-title">Font Size</div>
					  <div class="field-widget"><input id="font-legend-title" type="number" value="12" onchange="set_font(this.value, 'legend', 'size', 'title')"></div>                              
					</div>
					<div class="field">
					  <div class="field-title">Font Color</div>
					  <div class="field-widget">
						  <div class="input-group color colorpicker-element" data-color="#000000" data-color-format="hex" data-plugin-colorpicker="">
							<input id="img-tcolor-legend" type="color" class="input-group-addon color-pick" value="#000000" colorpick-eyedropper-active="false" data-change="title" data-elem="font">
							<input id="tcolor-legend" type="text" class="form-control" value="#000000" oninput="change_color_from_text(this)" data-change="title" data-elem="font">
						  </div> 
					  </div>                              
					</div>
				</div>
				<div class="group__heading">
					<span class="cp-grp-head">Text</span>
					<span class="cp-toggle-btn"><button type="button" class="mb-xs mt-xs mr-xs btn btn-xs btn-primary" onclick="toggle('cp-leg-text')">Toggle</button>
					</span>
				</div>				
				<div id="cp-leg-text">
					<div class="field">
					  <div class="field-title">Typeface</div>
					  <div class="field-widget">
						<select name="typeface" id="tf_lg_text" class="" onchange="set_font(this.value, 'legend', 'family', 'text')">
						  <option value="" disabled selected>Select an option</option>
						  <option value="Arial" style="font-family:Arial">Arial</option>
						  <option value="Courier New" style="font-family:'Courier New'">Courier New</option>
						  <option value="Open Sans" style="font-family:'Open Sans'">Open Sans</option>
						  <option value="Times New Roman" style="font-family:'Times New Roman'">Times New Roman</option>
						</select>                  
					  </div>                              
					</div>
					<div class="field">
					  <div class="field-title">Font Size</div>
					  <div class="field-widget"><input id="font-legend-text" type="number" value="12" onchange="set_font(this.value, 'legend', 'size', 'text')"></div>                              
					</div>                              
					<div class="field">
					  <div class="field-title">Font Color</div>
						  <div class="input-group color colorpicker-element" data-color="#000000" data-color-format="hex" data-plugin-colorpicker="">
							<input id="img-color-legend" type="color" class="input-group-addon color-pick" value="#000000" colorpick-eyedropper-active="false" data-change="text">
							<input id="color-legend" type="text" class="form-control" value="#000000" oninput="change_color_from_text(this)" data-change="text">
						  </div>                               
					</div> 
				</div> 
				<div class="group__heading">
					<span class="cp-grp-head">Box</span>
					<span class="cp-toggle-btn"><button type="button" class="mb-xs mt-xs mr-xs btn btn-xs btn-primary" onclick="toggle('cp-leg-box')">Toggle</button>
					</span>
				</div>
				<div id="cp-leg-box">             
					<div class="field">
					  <div class="field-title">Border Width</div>
					  <div class="field-widget"><input id="border-legend-width" type="number" value="0" min="0" onchange="set_thickness(this.value, 'legend')"></div>                              
					</div>  
					<div class="field">
					  <div class="field-title">Border Color</div>
					  <div class="field-widget">
						  <div class="input-group color colorpicker-element" data-color="#000000" data-color-format="hex" data-plugin-colorpicker="">
							<input id="img-bcolor-legend" type="color" class="input-group-addon color-pick" value="#000000" colorpick-eyedropper-active="false" data-change="bordercolor">
							<input id="bcolor-legend" type="text" class="form-control" value="#000000" oninput="change_color_from_text(this)" data-change="bordercolor">
						  </div>				  
					  </div>                              
					</div>                 
					<div class="field">
					  <div class="field-title">Background Color</div>
					  <div class="field-widget">
						  <div class="input-group color colorpicker-element" data-color="#E2E2E2" data-color-format="hex" data-plugin-colorpicker="">
							<input id="img-bgcolor-legend" type="color" class="input-group-addon color-pick" value="#E2E2E2" style="background-color:#e2e2e2" colorpick-eyedropper-active="false" data-change="lg-bg">
							<input id="bgcolor-legend" type="text" class="form-control" value="#E2E2E2" oninput="change_color_from_text(this)" data-change="lg-bg">
						  </div>				  
					  </div>                              
					</div>
				</div>
              </div>
            </div>
          </div>
        </div>        
      </div>                            
    </div>
  </section>
</div>