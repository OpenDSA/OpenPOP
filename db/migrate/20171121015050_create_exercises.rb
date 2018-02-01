class CreateExercises < ActiveRecord::Migration[5.1]
  def change
    create_table :exercises do |t|
      t.string :exercise_id
      t.text :code

      t.timestamps
    end
  end
end
