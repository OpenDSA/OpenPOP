class Answer < ApplicationRecord
  belongs_to :exercise
  has_one :trace
end
