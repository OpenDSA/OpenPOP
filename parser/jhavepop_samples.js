var sample1="Node h = Utils.createList('1','2','3',\"last\");\n" +
"Node n;\n" +
"Node p = null;\n" +
"Node q = last;\n" +
"Node r = new    Node('A',null);\n" +
"p = q;\n" +
"r.next = p;       h.info = 'Z';\n" +
"            r.next.info = h.next.next.info;";

 var sample2="Node head = " +
"        Utils.createList( 'A','A','B','C','C','C','D','D', \"tail\" );\n" +
"Node p1 = head;\n" +
"Node p2;\n" +
"while ( (p1!=null) && (p1.next !=null) )\n" +
"{\n" +
"  if (p1.info == p1.next.info)\n" +
"  {\n" +
"     p2 = p1.next;\n" +
"     p1.next = p1.next.next;\n" +
"  }\n" +
"  if ( p1.next == null) {\n" +
"     tail = p1;\n" +
"  } else {\n" +
"      if ( p1.info != p1.next.info )\n" +
"      {\n" +
"          p1 = p1.next;\n" +
"      }}}";

var sample3="Node head = Utils.createList( 'A','A','B','A','C','A',\"tail\" );\n" +
"Node p;\n" +
"Node temp;\n" +
"while ((head != null) && (head.info =='A')) { temp = head; head = head.next; }\n" +
"if (head == null) { tail = null; } else\n" +
"{\n" +
"  for( p = head; p.next != null; )\n" +
"  {\n" +
"     if (p.next.info == 'A') {\n" +
"         temp = p.next;\n" +
"         p.next =  p.next.next;\n" +
"     }\n" +
"     else {\n" +
"          p = p.next;}}}               tail = p;";
