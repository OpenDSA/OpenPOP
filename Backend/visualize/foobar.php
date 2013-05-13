<?php
$pgm = array(
"<b>&nbsp; </b><br><font size=\"-0\">",
" 1  Node head = Utils.createList( 'A','A','B','A','C','A',\"tail\" );",
" 2  Node p = null;",
" 3  while ( ( head != null ) &&",
" 4          ( head.info == 'A' ) )",
" 5    head = head.next;",
" 6  }",
" 7  if ( head == null ) {",
" 8    tail = null;",
" 9  } else {",
"10    for ( p = head ; p.next != null ; /* empty */ )",
"11    {",
"12      if ( p.next.info == 'A' ) {",
"13        p.next = p.next.next;",
"14      } else {",
"15        p = p.next;",
"16      }",
"17    }",
"18  }",
"19  tail = p;",
"</font>"
);
for($i = 0; $i < count($pgm); $i++){
if($i ==$line){
  if ($start != "") {
     $temp1 = substr($pgm[$i],0,$start);
     $temp2 = substr($pgm[$i],$start,$end - $start);
     $temp3 = substr($pgm[$i],$end);
     print("$temp1");
     print("<font color = 'red'>$temp2</font>");
     print("$temp3<br>");
  } else {
     print("<font color = 'red'>$pgm[$i]</font><br>");
 }
} else
print("$pgm[$i]<br>");
}
?>