var testvisualizerTrace = {"code":"Link p = createList(1,2,3); \nLink q = p.next(); \n\n p = q; \n\n \n ","trace":[{"stdout":"","event":"step_line","line":1,"stack_to_render":[{"func_name":"reAssignPointer:1","encoded_locals":{},"ordered_varnames":[],"parent_frame_id_list":[],"is_highlighted":true,"is_zombie":false,"is_parent":false,"unique_hash":"142","frame_id":142},{"func_name":"main:37","encoded_locals":{"SUCCESS":false},"ordered_varnames":["SUCCESS"],"parent_frame_id_list":[],"is_highlighted":false,"is_zombie":false,"is_parent":false,"unique_hash":"143","frame_id":143}],"globals":{},"ordered_globals":[],"func_name":"reAssignPointer","heap":{}},
{"stdout":"","event":"step_line","line":2,"stack_to_render":[{"func_name":"reAssignPointer:2","encoded_locals":{"p":["REF",478]},"ordered_varnames":["p"],"parent_frame_id_list":[],"is_highlighted":true,"is_zombie":false,"is_parent":false,"unique_hash":"168","frame_id":168},{"func_name":"main:37","encoded_locals":{"SUCCESS":false},"ordered_varnames":["SUCCESS"],"parent_frame_id_list":[],"is_highlighted":false,"is_zombie":false,"is_parent":false,"unique_hash":"169","frame_id":169}],"globals":{},"ordered_globals":[],"func_name":"reAssignPointer","heap":{"478":["INSTANCE","Link",["e",1],["n",["REF",476]]],"476":["INSTANCE","Link",["e",2],["n",["REF",474]]],"474":["INSTANCE","Link",["e",3],["n",null]],"475":3,"477":2,"479":1}},
{"stdout":"","event":"step_line","line":4,"stack_to_render":[{"func_name":"reAssignPointer:4","encoded_locals":{"p":["REF",478],"q":["REF",476]},"ordered_varnames":["p","q"],"parent_frame_id_list":[],"is_highlighted":true,"is_zombie":false,"is_parent":false,"unique_hash":"170","frame_id":170},{"func_name":"main:37","encoded_locals":{"SUCCESS":false},"ordered_varnames":["SUCCESS"],"parent_frame_id_list":[],"is_highlighted":false,"is_zombie":false,"is_parent":false,"unique_hash":"171","frame_id":171}],"globals":{},"ordered_globals":[],"func_name":"reAssignPointer","heap":{"476":["INSTANCE","Link",["e",2],["n",["REF",474]]],"474":["INSTANCE","Link",["e",3],["n",null]],"475":3,"477":2,"478":["INSTANCE","Link",["e",1],["n",["REF",476]]],"479":1}},
{"stdout":"","event":"step_line","line":4,"stack_to_render":[{"func_name":"reAssignPointer:4","encoded_locals":{"p":["REF",476],"q":["REF",476]},"ordered_varnames":["p","q"],"parent_frame_id_list":[],"is_highlighted":true,"is_zombie":false,"is_parent":false,"unique_hash":"176","frame_id":176},{"func_name":"main:37","encoded_locals":{"SUCCESS":false},"ordered_varnames":["SUCCESS"],"parent_frame_id_list":[],"is_highlighted":false,"is_zombie":false,"is_parent":false,"unique_hash":"177","frame_id":177}],"globals":{},"ordered_globals":[],"func_name":"reAssignPointer","heap":{"476":["INSTANCE","Link",["e",2],["n",["REF",474]]],"474":["INSTANCE","Link",["e",3],["n",null]],"475":3,"477":2}}],"userlog":"Debugger VM maxMemory: 807M \n "}
$(document).ready(function() { 
 
 	 var testvisualizer = new ExecutionVisualizer('testvisualizerDiv', testvisualizerTrace,{embeddedMode: false, lang: 'java', heightChangeCallback: redrawAllVisualizerArrows}); 
 
 	function redrawAllVisualizerArrows() { 
 
 	 	 if (testvisualizer) testvisualizer.redrawConnectors(); 
 	 } 
 
 $(window).resize(redrawAllVisualizerArrows); 
});