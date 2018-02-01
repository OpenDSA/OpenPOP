class ApplicationController < ActionController::Base
  protect_from_forgery with: :null_session

  def go
    redirect_to exercise_answer_path
  end
end
