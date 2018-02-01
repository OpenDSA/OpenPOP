class String
  def numeric?
    Float(self) != nil rescue false
  end
end
def generate_backend_trace(junit_test_file, files_path, peruser_files_path, student_file_name)
  raw_code = junit_test_file
  raw_code.gsub! "\n", "\\n" + "\n"
  raw_code.gsub! "\t", "\\t"
  lines = raw_code.split("\n")
  jUnit_test = ""
  lines.each {|line| jUnit_test = jUnit_test + line}
  jUnit_test.gsub!('\"', "\\" + '\"')
  student_file = File.open(File.join(File.dirname(File.expand_path( __FILE__)),peruser_files_path, student_file_name), "w+")
  #puts "file path #{student_file.path}"
  fullString = '{' + "\n" + '"' + "usercode" + '"' + ':' + '"' + jUnit_test + '"' +
      ',' + "\n" + '"' + "options" + '"' + ':' + '{' + '}' + ',' +
      "\n" + '"' + "args" + '"' + ':' + '[' + ']' + ',' + "\n" + '"' +
      "stdin" + '"' + ':' + '"' + '"' + "\n" + '}'
  student_file.puts(fullString)
  student_file.close
  #puts "student file #{fullString}"
  #Dir.chdir "/home/mdn/Research/OpenDSA-DevStack/OpenPOP/Java-Visualizer/frontAndBackendFiles/backendFiles"
  #output = `./java/bin/java -cp .:cp:cp/javax.json-1.0.jar:java/lib/tools.jar traceprinter.InMemory < cp/traceprinter/output.txt` # the shell command
  output = `java -cp .:cp:cp/javax.json-1.0.4.jar:java/tools.jar traceprinter.InMemory < cp/traceprinter/output.txt` # the shell command
  #puts output
  return output

end

def seperate_and_filter_trace(junit_test_file, files_path, peruser_files_path, student_file_name)
  code_and_trace = generate_backend_trace(junit_test_file, files_path, peruser_files_path,
                                          student_file_name)
  splitter = '"' + "trace" + '"' + ':'
  user_code, whole_trace = code_and_trace.split(splitter)

  whole_trace = whole_trace[1..whole_trace.length]

  entire_json_file = code_analyzer(user_code, whole_trace)

  return entire_json_file
end

class Event
  attr_accessor :trace, :line_number

  def initialize()
    @trace = ""
    @line_number = 0
  end

  def set_line(line_number)
    @line_number = line_number
  end

  def set_event(trace)
    @trace = trace
  end
end

class EventManager
  attr_accessor :list_of_events, :filtered_events

  def initialize
    @list_of_events = []
    @filtered_events = []
  end

  def get_line_number(index)
    if @list_of_events.length == 0
      puts "list is empty"
    else
      temp_event = @list_of_events[index]
      return temp_event.line_number
    end
  end

  def set_event (index, event)
    @filtered_events[index] = event
  end

  def get_event(index)
    return @filtered_events[index]
  end

  def add_event(event)
    @list_of_events << event
  end

  def trace_list
    my_list = []
    (0...@filtered_events.length).each do |x|
      #temp = Event.new
      temp = @filtered_events[x]
      my_list<<temp.trace
    end
    return my_list
  end

  def print_events
    if @filtered_events.length == 0
      puts 'List of events is empty'
    else
      (0..@filtered_events.length).each do |x|
        temp_event = @filtered_events[x]
        puts temp_event.trace
      end
    end
  end

  def verify_events
    event_counter = 0
    counter = 1
    original_line_num = get_line_number(0)
    current_line = original_line_num
    length = @list_of_events.length - 1
    while counter < length + 1
      next_line = get_line_number(counter)
      if (current_line + 1 == next_line && next_line > original_line_num) || (
      current_line + 2 == next_line && next_line > original_line_num) || (
      current_line + 3 == next_line && next_line > original_line_num) || (
      current_line + 4 == next_line && next_line > original_line_num) || (
      current_line + 5 == next_line && next_line > original_line_num)
        @filtered_events << @list_of_events[event_counter]
        event_counter += 1
        current_line = next_line
        counter += 1
      else
        current_line = next_line
        event_counter += 1
        counter += 1
      end
    end
    @filtered_events << @list_of_events[length]
  end

  def modify_lines (code)
    line_number = 0
    event_number = 0

    while line_number != code.length
      #modify = Event.new
      #temp_string = ""
      #temp_line = 0

      modify = @filtered_events[event_number]
      temp_string = modify.trace
      temp_line = modify.line_number

      if code[line_number] == "newline"
        line_number += 1
      elsif code[line_number] == "\\t"
        line_number += 1
      else
        original_line = temp_line.to_s
        new_line = (line_number + 1).to_s
        temp_string.gsub! original_line, new_line
        modified_event = Event.new
        modified_event.set_event(temp_string)
        modified_event.set_line(line_number + 1)
        @filtered_events[event_number] = modified_event

        event_number = event_number + 1
        line_number = line_number + 1
      end
    end
    #last_event = Event.new
    last_event = @filtered_events[event_number]
    temp_line = last_event.line_number
    temp_string = last_event.trace
    old_line = temp_line.to_s
    second_tl_event = @filtered_events[event_number - 1]
    other_line = second_tl_event.line_number
    new_line = other_line.to_s
    temp_string = temp_string.gsub old_line, new_line
    modified_event = Event.new
    modified_event.set_event(temp_string)
    modified_event.set_line(other_line)
    @filtered_events[event_number] = modified_event
  end

end

def modify_stack (my_list)
  old_stack = []
  curly_stack = []
  list_of_stack_points = []

  (0...my_list.length).each do |x|
    cur_event = my_list[x].split("stack_to_render\":[")
    stacks = cur_event[1].split("],\"globals\"")

    stack_to_render = stacks[0]
    old_stack<< stacks[0]

    stack_point = ''

    for i in stack_to_render.split('') do
      stack_point += i
      if i == '{'
        curly_stack << i
      elsif i == '}'
        top_symbol = curly_stack.pop
        if curly_stack.length == 0
          list_of_stack_points << stack_point
          stack_point = ''
        else
          next
        end
      end
    end
  end

  main = 'main:'

  new_stack = []

  (0...list_of_stack_points.length).each do |x|
    if list_of_stack_points[x].include? main
      # Do nothing
      next
    else
      new_stack << list_of_stack_points[x]
    end
  end

    (0...my_list.length).each do |x|
      my_list[x].gsub!(old_stack[x], new_stack[x])
    end
  return my_list
end

class Trace_analyzer
  def initialize
    @event_manager = EventManager.new
  end

  def handleEverything(user_code, in_trace)
    puts in_trace
    exe_Point_Finder (in_trace)
    @event_manager.verify_events
    @event_manager.modify_lines(user_code)

    raw_events = @event_manager.trace_list

    clean_events = modify_stack(raw_events)
    #puts clean_events
    print_to_file = ''
    # At this point, everything is ready for output. The printToFile string
    # contains all of the information necessary for the javaScript file.
    # Its about 20 lines down
    #path = File.join(File.dirname(File.expand_path('..', __FILE__)),'frontendFiles', 'filteredJSON.js')
    #f = File.new(path, "w+")
      first = "var testvisualizerTrace = {\"code\":\""
      code = ""
      (0...user_code.length).each do |x|
        if user_code[x] == "newline"
          code = code + "\\n" + " "
        else
          code = code + user_code[x] + "\\n"
        end
      end


      second = "\",\"trace\":["

      trace = ""
      (0...clean_events.length).each do |y|
        if y == clean_events.length - 1
          temp_string = clean_events[y]
          temp_string = temp_string[0...-1]
          trace = trace + temp_string
          trace = trace + "],\"userlog\":\"Debugger VM maxMemory: 807M \\n \"}"
          trace = trace + "\n\n" + "$(document).ready(function() { \n \n \t var testvisualizer = new ExecutionVisualizer('testvisualizerDiv', testvisualizerTrace,{embeddedMode: false, lang: 'java', heightChangeCallback: redrawAllVisualizerArrows}); \n \n \tfunction redrawAllVisualizerArrows() { \n \n \t \t if (testvisualizer) testvisualizer.redrawConnectors(); \n \t } \n \n $(window).resize(redrawAllVisualizerArrows); \n});"
        else
          temp_string = clean_events[y]
          trace = trace + temp_string + "\n"
        end
      end


      # String that contains everything for the javascript file
      # Maybe just send string to front end and write to file in
      # a directory accessible by the OpenDSA frontend?
      print_to_file = first + code + second + trace
      #f.print (print_to_file)


    #f.close


    return clean_events# it should be print_to_file
  end

  def is_empty(any_structure)
    if any_structure.length != 0
      return false
    else
      return true
    end
  end

  def extract_Line_Num(string)

    line = string.gsub '"', ' '
    line.gsub! '{', ' '
    line.gsub! ':', ' '
    line.gsub! ',', ' '
    line.gsub! '[', ' '
    line.gsub! '(', ' '
    line.gsub! ']', ' '
    line.gsub! '}', ' '
    line.gsub! ')', ' '

    new_line = []
    for s in line.split() do
      if s.numeric?
        new_line << s.to_i
      end
    end

    return new_line[0]

  end

  def verify_exe_point(on, off, in_point)

    add_exe_point = false
    exe_trace = Event.new

    if on == true && off == false
      exe_trace.set_event(in_point)
      exe_trace.set_line(extract_Line_Num(in_point))
      @event_manager.add_event(exe_trace)
      add_exe_point = true

    elsif on == false && off == false
      add_exe_point = false
    else
      add_exe_point = false
    end

    return add_exe_point
  end

  def exe_Point_Finder(trace)
    symbol_stack = []
    other_list = []
    current_symbol = ''
    top_symbol = ''
    exe = ''
    exe_point = ' '
    on = false
    off = false

    for i in trace.split('') do
      current_symbol = i
      exe_point += current_symbol
      if i == '{' or i == '[' or i == '('
        symbol_stack << i
      elsif i == '}' or i == ')' or i == ']'
        if is_empty(symbol_stack) == false
          top_symbol = symbol_stack.pop
          if i == '}' and top_symbol != '{'
            next
          end
        end
      elsif i == ','
        other_list << exe_point
        if symbol_stack.length == 0
          for thing in other_list do
            exe += thing
          end
          if exe.include? 'startTraceNow'
            on = true
            exe = ''
            exe_point = ''
            other_list = []
          elsif exe.include? 'endTraceNow'
            off = true
            return
          else
            flag = verify_exe_point(on, off, exe)
            if flag == true
              exe = ''
              exe_point = ''
              other_list = []
            else
              on = false
              exe = ""
              exe_point = ''
              other_list = []
            end
          end

        else
          exe_point = ""
        end

      else
        next
      end
    end
  end
end

def is_empty(structure)
  if structure.length == 0
    return true
  else
    return false
  end
end

def code_splitter(code)
  student_code = []

  code = code.split("startTraceNow();")
  new_code = code[1].split("endTraceNow();")

  executed_code = new_code[0]

  executed_code_list = executed_code.split("\\n")

  flag = false
  counter = 0

  until flag
    if executed_code_list[counter] == '' or executed_code_list[counter] == ' '
      flag = false
      counter += 1
    elsif executed_code_list[counter] != ''
      flag = true
    end
  end

  x = counter
  while x<executed_code_list.length
    temp = executed_code_list[x]
    temp = temp.strip

    if temp.empty?
      student_code << 'newline'
    else
      student_code << executed_code_list[x]
    end
    x +=1
  end


  return student_code
end

def code_analyzer(code, first_trace)
  code_to_viz = []
  code_to_viz = code_splitter(code)

  trace_analyzer = Trace_analyzer.new

  execute = trace_analyzer.handleEverything(code_to_viz, first_trace)

  return execute
end


def main_method (file_path, student_full_code)
  my_test = seperate_and_filter_trace(student_full_code, file_path, "cp/traceprinter/", "output.txt")
  #html1 = File.open("htmlOutput1.txt", 'r')
  #html2 = File.open("htmlOutput2.txt", 'r')
  #path = File.join(File.dirname(File.expand_path('..', __FILE__)),'frontendFiles', 'result.html')
  #output = File.new(path, 'w+')
  #output.write(html1.read + my_test + html2.read)
  Dir.chdir('/home')
  #puts my_test
  return my_test
end

def create_student_full_code (code)
  @student_code = ''
  #File.open('test22.txt', 'rb') do |code_file|
  #  code = code_file.read()
    code = code.split('return')[0].split('{')[1]
    code = code.split("\r\n")
    code.each do |line|
      unless line.empty?
        @student_code += line + "\n"
      end
  #  end

  end
  #puts Dir.pwd
  File.open('codePart1.txt', 'rb') do |part1File|
    @part1 = part1File.read
  end
  File.open('codePart2.txt', 'rb') do |part2File|
    @part2 = part2File.read
  end
  full_student_code = @part1 + @student_code + "\n" + @part2

return main_method("", full_student_code)
end

#student_code = create_student_full_code()
#main_method(" ", student_code)
#Dir.chdir "/home/mdn/Research/OpenDSA-DevStack/OpenPOP/Java-Visualizer/frontAndBackendFiles/backendFiles"
#output = `./java/bin/java -cp .:cp:cp/javax.json-1.0.jar:java/lib/tools.jar traceprinter.InMemory < cp/traceprinter/output.txt` # the shell command
#backend_trace = output
#puts backend_trace
#create_student_full_code("{int c = 1000; \n return 10;}")
