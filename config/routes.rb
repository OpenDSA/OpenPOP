Rails.application.routes.draw do
  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
  #get 'answers/visualize' => 'answers#visualize'
  get 'answers/visualize/exercises/:exercise_id/answers/:id' => 'answers#visualize', as: 'visualize'
  post 'answers/solve/' => 'answers#solve', as: 'solve'
  #get 'answers/solve/:exercise_id' => 'answers#solve', as: 'solve'

  resources :exercises do
    resources :answers do
      resource :trace
    end
  end

end
