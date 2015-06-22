/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package jsonfilter;
 
import java.io.*;
import java.util.Stack;
import java.lang.Object; 
import java.util.Scanner; 
import java.util.Arrays;
import java.util.ArrayList; 
import java.lang.String;
import java.nio.ByteBuffer;


/**
 *
 * @author Kyle Reinholt 
 * 
 * @purpose This program will read in a json text file, filter out the execution points that are between the function startTraceNow() and endTraceNow(), 
 *          and output the filtered to execution points to be sent to the executionVisualizer in the javaScript page for Java Visualizer. 
 * 
 *
 */

class Event {
    
    private int lineNumber; 
    private String trace; 
    
    Event() { 
        
        lineNumber = 0; 
        trace = ""; 
    }
    
    public void setEvent(String exePoint){
        
        trace = exePoint; 
    }
    
    public void setLineNumber(int line) { 
        
        lineNumber = line; 
    }
    
    public String getEvent() { 
        
       return trace; 
    }
    
    public int getLineNumber() { 
        
        return lineNumber; 
    }
    
    
}

class EventManager { 
    
    private ArrayList<Event> listOfEvents;
    private ArrayList<Event> filteredEvents; 
    
    EventManager() {
        
        listOfEvents = new ArrayList<>();
        filteredEvents = new ArrayList<>(); 
    }
    
    public int getNumOfEvents() {
        
        return filteredEvents.size(); 
    }
    
    public Event getEvent(int index){
        
        return filteredEvents.get(index);  
    }
    
    public void addEvent(Event newEvent) {
        
        listOfEvents.add(newEvent); 
    }
    
    public void modifyLineNums() {
        
        for(int n = 0; n < filteredEvents.size(); n++) {
            
           Event modify = new Event(); 
           String tempString = ""; 
           int tempLine = 0; 
           
           modify = filteredEvents.get(n); 
           
           tempString = modify.getEvent(); 
           
           tempLine = modify.getLineNumber(); 
           
           if(n == filteredEvents.size() - 1){
               
                String originalLine = Integer.toString(tempLine);
                String newLine = Integer.toString(n);
                
                tempString = tempString.replace(originalLine, newLine);

                filteredEvents.get(n).setEvent(tempString);
           }
           else{
               
               String originalLine = Integer.toString(tempLine);
               String newLine = Integer.toString(n+1);
           
               tempString = tempString.replace(originalLine, newLine);

               filteredEvents.get(n).setEvent(tempString);
           }
        }
    }
    
    public void printAllLines(){
        
        for(int i = 0; i < listOfEvents.size(); i++) {
            
            
            System.out.print("Line number: "); 
            System.out.print(listOfEvents.get(i).getLineNumber()); 
            System.out.println();  
        }
    }
    
    public void printFilteredEvents(){
        
        for(int l = 0; l < filteredEvents.size(); l++) {
           
            System.out.print("Line number: "); 
            System.out.print(filteredEvents.get(l).getLineNumber()); 
            System.out.println();  
        }
    }
    
    public void verifyEvents() { 
        
        int currentLine = 0;
        int nextLine = 0; 
        int eventCounter = 0; 
        
        int originalLine = listOfEvents.get(0).getLineNumber(); 
        
        currentLine = listOfEvents.get(0).getLineNumber(); 
        
        for(int k = 1; k < listOfEvents.size(); k++) {
            
            nextLine = listOfEvents.get(k).getLineNumber(); 
            
            if(currentLine+1 ==  nextLine && nextLine > originalLine || currentLine+2 ==  nextLine && nextLine > originalLine || currentLine+3 ==  nextLine && nextLine > originalLine  || currentLine+4 ==  nextLine && nextLine > originalLine || currentLine+5 ==  nextLine && nextLine > originalLine  || currentLine+6 ==  nextLine && nextLine > originalLine ){
                
                filteredEvents.add(listOfEvents.get(eventCounter));
                eventCounter = eventCounter + 1; 
                currentLine = nextLine;
  
            }
            else { 
                
                currentLine = nextLine;
                eventCounter = eventCounter + 1; 
                
            }
            
            
        }
        
        filteredEvents.add(listOfEvents.get(listOfEvents.size()-1)); 
       
    }
    
}

class CodeAnalyzer { 
    
    private String codeTrace; 
    private ArrayList<String> codeList; 
    
    CodeAnalyzer() {
        
    }
    
    CodeAnalyzer(String jsonCode) {
        
        codeList = new ArrayList<>(); 
        //System.out.println(jsonCode);
        setCodeTrace(jsonCode);  
    }
    
    public ArrayList getCodeList() {
        
        return codeList; 
    }
    
    public void setCodeTrace(String json){
        
        codeTrace = json; 
    }
    
    public void isolateStudentCode(){
        
        String modify = codeTrace; 
        
        String[] isolateMain = modify.split("main"); //retrieves everything after main function. We are only conserned with code that is being executed within main.  
        
        String[] isolateStart = isolateMain[1].split("startTraceNow\\(\\)\\;"); //This will grab everything after startTrace4
        
        String[] isolateEnd = isolateStart[1].split("endTraceNow\\(\\)\\;");
        
        String myCode = isolateEnd[0];
        
        String newLine = myCode.replace("\\n", "newline"); 
        
        String myString = newLine.replaceFirst("newline", ""); 
        
        myString = myString.trim(); 
        
        String[] studentCode = myString.split("newline"); 
        
        for(int o = 0; o < studentCode.length; o++){
            
            if(studentCode[o].isEmpty() == true){
                
                // don nothing
            }
            else if(studentCode[o].length() < 3) {
                
                System.out.println("newline detected.");
            }
            else{
                
                codeList.add(studentCode[o]);
                codeList.get(o).trim(); 
                System.out.println(studentCode[o]); 
            }
             
        }
        
    }
    
  
}

class TraceAnalyzer {
    
    private String originalTrace; 
    private Stack<Character> symbolStack;
    private ArrayList<String> exePointList;  
    private int executionPoints; //integer counter of how many execution points there are
    //private FileOutputStream out;
    private UniqueFileWriter jsonWriter;
    private EventManager eventManager; 
    
    TraceAnalyzer() {
        
    }
    
    TraceAnalyzer(String jsonTrace) {
        
        originalTrace = jsonTrace;
        exePointList = new ArrayList<>();
        eventManager = new EventManager(); 
        executionPoints = 0; 
    }
    
    public void curlyBraceTest() { 
        
        String copyTrace = originalTrace; 
        String executionPoint = ""; 
        
        boolean startSwitch = false; 
        boolean endSwitch = false;
        
        symbolStack = new Stack<>();
        
        for (int index = 0; index < copyTrace.length(); index++) {
            char currentSymbol = copyTrace.charAt(index);
            executionPoint = executionPoint + currentSymbol; 
            switch (currentSymbol) {
            case '(':
            case '[':
            case '{': 
                symbolStack.push(currentSymbol);
                break;

            case ')':
            case ']':
            case '}':
                if (!symbolStack.isEmpty()) {
                    char symbolStackTop = symbolStack.pop();
                    if ((currentSymbol == '}' && symbolStackTop != '{')
                            || (currentSymbol == ')' && symbolStackTop != '(')
                            || (currentSymbol == ']' && symbolStackTop != '[')) {
                        System.out.println("Unmatched closing bracket while parsing " + currentSymbol + " at " + index+1);
                        return;
                    }
                } else {
                    System.out.println("Extra closing bracket while parsing " + currentSymbol + " at character " + index+1);
                    return;
                }
                break;
            case ',': 
                 if ( symbolStack.size() == 0)
                 {
                     executionPoint = executionPoint.substring(0, executionPoint.length()-1); //This removes the trailing comma at the end of each exePoint
                     if( executionPoint.contains("startTraceNow")){
                         
                         startSwitch = true; 
                         //verifyExePoint(startTrace,endTrace,executionPoint);
                         executionPoint = "";
                     }
                     else if( executionPoint.contains("endTraceNow")){
                         
                         endSwitch = true;
                         break; 
                     }
                     else 
                     {
                         if(verifyExePoint(startSwitch,endSwitch,executionPoint)){
                             
                             executionPoints = executionPoints + 1; //integer counter of how many execution points there are
                             executionPoint = ""; 
                         }
                         else {
                             
                             executionPoint = ""; 
                         }
                      
                     }
                                                           
                 }
                 else 
                 {
                     
                 }
                 break; 
                 
            default:
                break;
            }
        }
        
        
       
       
        
    }
    
    public void handleEvents() { 
        
       eventManager.verifyEvents();
       eventManager.printFilteredEvents();
       eventManager.modifyLineNums();
    }
    
    public void outputFilteredJSON(ArrayList<String> inList) {
        
        jsonWriter = new UniqueFileWriter();
        
        jsonWriter.writeToFile("{" + '"' + "code" + '"' + ':' + '"');
        for(int p = 0; p < inList.size(); p++) {
            
            jsonWriter.writeToFile(inList.get(p));
            jsonWriter.writeToFile("\\n");
        }
        
        jsonWriter.writeToFile("" + '"' + ',' + '"' + "trace" + '"' + ':' + '[');
        
        for( int m = 0; m < eventManager.getNumOfEvents(); m++){
            
            Event myEvent = new Event();  
            myEvent = eventManager.getEvent(m);
            
            if( m == eventManager.getNumOfEvents() - 1)
            {
                jsonWriter.writeToFile(myEvent.getEvent());
                jsonWriter.writeToFile("]" + ',' + '"' + "userlog" + '"' + ":" + '"' + "Debugger VM maxMemory: 807M" + "\\n" + '"' + "}");
            }
            else 
            {
                jsonWriter.writeToFile(myEvent.getEvent());
                jsonWriter.writeToFile(",");
                jsonWriter.writeToFile("\n");
                jsonWriter.flushFile();
            }
           
        }
        
        jsonWriter.closeFile();
    
    }
    
    public void printExecutionTraces(){
        
        //Test function
        
        for(int i = 0; i < exePointList.size(); i++){
            
            System.out.println(exePointList.get(i)); 
        }
    } 
    
    public void numOfExePnts(){
        
        System.out.print("There are: "); 
        System.out.print( executionPoints ); 
        System.out.print(" Execution Points."); 
    }
    
    public boolean verifyExePoint(boolean on, boolean off, String inPoint) {
        
        boolean addExePoint = false; 
        Event exeTrace = new Event(); 
        
        if(on == true && off == false) //If the exePoint makes it here, it qualifies as an event, however, the event must then be verified by the event manager
        {
            exePointList.add(inPoint);  
            exeTrace.setEvent(inPoint);
            exeTrace.setLineNumber(extractLineNum(inPoint));
            System.out.println(extractLineNum(inPoint)); 
            eventManager.addEvent(exeTrace);
            addExePoint = true; 
        }
        else if(on == false && off == false) 
        {
            addExePoint = false; 
        }
        else 
        {
            addExePoint = false; 
        }
        
        return addExePoint;
    }
    
    public int extractLineNum(String input){
        
        int lineNumber = 0; 
        
        lineNumber = new Scanner(input).useDelimiter("\\D+").nextInt();
        
        return lineNumber; 
    }
    

}

class UniqueFileWriter{
    
    private File filteredTrace = new File("filteredJSON.txt"); 
    private FileWriter fw; 
    
    UniqueFileWriter() {
        
          try{
        
           fw = new FileWriter(filteredTrace);
           
       }catch (IOException iox) {
            //do stuff with exception
            iox.printStackTrace();
        } 
    }
    
    public void flushFile() { 
        
       try {  
        
           fw.flush();
           
       }catch (IOException iox) { 
           
           iox.printStackTrace();
       }
    }
    
    public void closeFile() { 
        
       try{
            
           fw.close();
           
       }catch (IOException iox) {
        
           iox.printStackTrace(); 
       }
       
    }
    
    public void writeToFile(String input) { 
        
        
         try{
            
           fw.write(input);
           
       }catch (IOException iox) {
        
           iox.printStackTrace(); 
       }
    }
}

class UniqueFileReader{ 
    
    private int lineNumber; 
    private CodeAnalyzer analyzeCode; 
    private TraceAnalyzer analyzeTrace; 
    
    UniqueFileReader(String inputFile) {
        lineNumber = 0; 
        
        readFile(inputFile); 
    }
    
    public void readFile(String fileName) {     

        String jsonFile = fileName;

        String line = null; 
        String lineCopy = null; 

        try {
            // FileReader reads text files in the default encoding.
            FileReader fileReader = 
                new FileReader(jsonFile);

            // Always wrap FileReader in BufferedReader.
            BufferedReader bufferedReader = 
                new BufferedReader(fileReader);

            while((line = bufferedReader.readLine()) != null) {
                
                lineCopy = line; 
                
                String splitter = "" + '"' + ',' + '"';
                String traceSplitter = "" + '"' + "trace" + '"' + ':'; 
                
                String[] jsonCode = line.split(splitter);
                String[] jsonTrace = lineCopy.split(traceSplitter);
                
                splitter = "" + '"' + ':' + '"'; 
                
                String[] codeSection = jsonCode[0].split(splitter); 
                
                String codeSegment = codeSection[1]; 
                String traceSegment = jsonTrace[1]; 
                
                analyzeCode = new CodeAnalyzer(codeSegment);
                analyzeTrace = new TraceAnalyzer(traceSegment.substring(1));
                
                analyzeTrace.curlyBraceTest(); 
                analyzeTrace.handleEvents();
                
                
                analyzeCode.isolateStudentCode();
                
      
                analyzeTrace.outputFilteredJSON(analyzeCode.getCodeList()); //passing in the code trace to be printed to the file 
                                                                            // before the execution points. 
                //analyzeTrace.printExecutionTraces();
                //analyzeTrace.numOfExePnts(); 
                
            }    

            // Always close files.
            bufferedReader.close();            
        }
        catch(FileNotFoundException ex) {
            System.out.println(
                "Unable to open file '" + 
                jsonFile + "'");                
        }
        catch(IOException ex) {
            System.out.println(
                "Error reading file '" 
                + jsonFile + "'");                   
            // Or we could just do this: 
            // ex.printStackTrace();
        }

    }
    
    public void writeFile(){
        
        
    }

}

public class JsonFilter {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // TODO code application logic here
        
        UniqueFileReader myFileReader = new UniqueFileReader("jsonfile.txt");
        
        
    }
    
}
