var testvisualizerTrace = {"code":"Link p = createList(1,2,3); \n Link r = p.next().next(); \n p = p.next(); \n","trace":[{"stdout":"","event":"step_line","line":1,"stack_to_render":[{"func_name":"reAssignPointer:1","encoded_locals":{},"ordered_varnames":[],"parent_frame_id_list":[],"is_highlighted":true,"is_zombie":false,"is_parent":false,"unique_hash":"142","frame_id":142},{"func_name":"main:25","encoded_locals":{"SUCCESS":false},"ordered_varnames":["SUCCESS"],"parent_frame_id_list":[],"is_highlighted":false,"is_zombie":false,"is_parent":false,"unique_hash":"143","frame_id":143}],"globals":{},"ordered_globals":[],"func_name":"reAssignPointer","heap":{}},
{"stdout":"","event":"step_line","line":2,"stack_to_render":[{"func_name":"reAssignPointer:2","encoded_locals":{"p":["REF",478]},"ordered_varnames":["p"],"parent_frame_id_list":[],"is_highlighted":true,"is_zombie":false,"is_parent":false,"unique_hash":"188","frame_id":188},{"func_name":"main:25","encoded_locals":{"SUCCESS":false},"ordered_varnames":["SUCCESS"],"parent_frame_id_list":[],"is_highlighted":false,"is_zombie":false,"is_parent":false,"unique_hash":"189","frame_id":189}],"globals":{},"ordered_globals":[],"func_name":"reAssignPointer","heap":{"478":["INSTANCE","Link",["e",1],["n",["REF",476]]],"476":["INSTANCE","Link",["e",2],["n",["REF",474]]],"474":["INSTANCE","Link",["e",3],["n",null]],"475":3,"477":2,"479":1}},
{"stdout":"","event":"step_line","line":3,"stack_to_render":[{"func_name":"reAssignPointer:3","encoded_locals":{"p":["REF",478],"r":["REF",474]},"ordered_varnames":["p","r"],"parent_frame_id_list":[],"is_highlighted":true,"is_zombie":false,"is_parent":false,"unique_hash":"214","frame_id":214},{"func_name":"main:25","encoded_locals":{"SUCCESS":false},"ordered_varnames":["SUCCESS"],"parent_frame_id_list":[],"is_highlighted":false,"is_zombie":false,"is_parent":false,"unique_hash":"215","frame_id":215}],"globals":{},"ordered_globals":[],"func_name":"reAssignPointer","heap":{"474":["INSTANCE","Link",["e",3],["n",null]],"475":3,"478":["INSTANCE","Link",["e",1],["n",["REF",476]]],"476":["INSTANCE","Link",["e",2],["n",["REF",474]]],"477":2,"479":1}},
{"stdout":"","event":"step_line","line":3,"stack_to_render":[{"func_name":"reAssignPointer:3","encoded_locals":{"p":["REF",476],"r":["REF",474]},"ordered_varnames":["p","r"],"parent_frame_id_list":[],"is_highlighted":true,"is_zombie":false,"is_parent":false,"unique_hash":"216","frame_id":216},{"func_name":"main:25","encoded_locals":{"SUCCESS":false},"ordered_varnames":["SUCCESS"],"parent_frame_id_list":[],"is_highlighted":false,"is_zombie":false,"is_parent":false,"unique_hash":"217","frame_id":217}],"globals":{},"ordered_globals":[],"func_name":"reAssignPointer","heap":{"474":["INSTANCE","Link",["e",3],["n",null]],"475":3,"476":["INSTANCE","Link",["e",2],["n",["REF",474]]],"477":2}}],"userlog":"Debugger VM maxMemory: 807M\n"}
$(document).ready(function() { 
 
 	 var testvisualizer = new ExecutionVisualizer('testvisualizerDiv', testvisualizerTrace,{embeddedMode: false, lang: 'java', heightChangeCallback: redrawAllVisualizerArrows}); 
 
 	function redrawAllVisualizerArrows() { 
 
 	 	 if (testvisualizer) testvisualizer.redrawConnectors(); 
 	 } 
 $(window).resize(redrawAllVisualizerArrows); 
});