
class AnswersController < ApplicationController

  respond_to :json, :html
  def create
    if @exercise.nil? and @answer.nil?
      @exercise = Exercise.find(params[:exercise_id])
      @answer = @exercise.answers.create(answer_params)
    end

    redirect_to exercise_path(@exercise)
    end

  def destroy
    @exercise = Exercise.find(params[:exercise_id])
    @answer = @exercise.answers.find(params[:id])
    if @answer.trace.nil?
      @answer.destroy
    else
      @answer.trace.destroy
      @answer.destroy
    end
    redirect_to exercise_path(@exercise)
  end

  def visualize
    #puts params.inspect
    @exercise = Exercise.find(params[:exercise_id])

    @answer = @exercise.answers.find(params[:id])
    #puts @answer.trace
    if @answer.trace.nil?
      #puts"new trace created"
      #puts @answer.trace
      trace = generate_code_trace(@exercise.code, @answer.StudentCode)
      @trace = @answer.create_trace(exercise_trace: trace)
    else
      #puts"old trace used"
      @trace = @answer.trace
    end
    #puts @trace.exercise_trace
    @openpop_results = build_visualization(@trace.exercise_trace, @answer.StudentCode)
  end

  def solve
    @exercise = Exercise.find_by_exercise_id(params[:exercise_id])
    student_answer = params[:code]
    student_answer = student_answer[student_answer.index('{')+1..student_answer.index('return')-1]
    @answer = Answer.find_by_StudentCode(student_answer)
    if @answer.nil?
      #puts"new one created"
      @answer = @exercise.answers.create(StudentCode: student_answer)
    end
    if @answer.trace.nil?
      #puts"new trace created"
      trace = generate_code_trace(@exercise.code, student_answer)
      @trace = @answer.create_trace(exercise_trace: trace)
    else
      #puts"old trace used"
        @trace = @answer.trace
    end
    #puts @trace.exercise_trace
    #results = JSON.parse('[' + trace + ']')
    #respond_with json: trace
    respond_to do |format|
      format.json { render :json => @trace }  # note, no :location or :status options
    end

  end


  def oldsolve
    id = params[:exerciseByID]
    solution = params[:solution]
    @exercise = Exercise.find_by_exercise_id(id)
    @answer = Answer.create(StudentCode: solution)
    #puts @exercise.code
    @answer = @exercise.answers.create(StudentCode: solution)
    redirect_to "/answers/visualize/exercises/#{@exercise.id}/answers/#{@answer.id}"
  end

  private
  def answer_params
    params.require(:answer).permit(:StudentCode)
  end

  def generate_code_trace(exercise, code)
    wrapper_code = exercise#@exercise.code
    answer_text = code #@answer.StudentCode
    path = File.join(File.dirname(File.expand_path('../..', __FILE__)), 'Java-Visualizer')
    pwd = Dir.pwd
    Dir.chdir path
    require path + '/' + 'RubyJsonFilter.rb'
    code_body = wrapper_code.sub(/\b__\b/, answer_text)
    code_body.gsub! "\r",''
    code_body.gsub! '\r',''
    code_trace = main_method('',code_body)
    #remove the last comma
    #trace = ""
    #(0...code_trace.length).each do |y|
    #  if y == code_trace.length - 1
    #    temp_string = code_trace[y]
    #    temp_string = temp_string[0...-1]
    #    trace = trace + temp_string
    #  else
    #    temp_string = code_trace[y]
    #    trace = trace + temp_string + "\n"
    #  end
    #end
    #results = "<script>" + codeTrace.split('$')[0] + "</script>"
    ##@openpop_results = "<script>" + create_student_full_code('{p=r;\n return 0;}').split('$')[0] + "</script>"
    #results.sub!('$', '</script><script> $')
    #@openpop_results = results
    #Dir.chdir pwd
    #return trace
    code_trace
  end

  def build_visualization(trace, student_code)
    first = "var testvisualizerTrace = {\"code\":\"" + student_code
    second = "\",\"trace\":[" + trace
    last = "],\"userlog\":\"Debugger VM maxMemory: 807M \\n \"}" +
        "\n\n" + "$(document).ready(function()" +
        "{ \n \n \t var testvisualizer = new ExecutionVisualizer('testvisualizerDiv'," +
        " testvisualizerTrace,{embeddedMode: false, lang: 'java', heightChangeCallback: redrawAllVisualizerArrows});"+
        " \n \n \tfunction redrawAllVisualizerArrows()"+
        " { \n \n \t \t if (testvisualizer) testvisualizer.redrawConnectors(); \n \t } "+
        "\n \n $(window).resize(redrawAllVisualizerArrows); \n});"
    return "<script>" + first + second + last + "</script>"
  end

end
