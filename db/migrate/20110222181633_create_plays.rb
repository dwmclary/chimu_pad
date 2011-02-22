class CreatePlays < ActiveRecord::Migration
  def self.up
    create_table :plays do |t|
      t.integer :match_id, :null => false
      t.integer :player_id, :null => false
      t.string  :position
      t.integer :shots
      t.integer :goals
      t.integer :passes_attempted
      t.integer :passes_completed
      t.float   :rating
      t.timestamps
    end
  end

  def self.down
    drop_table :plays
  end
end
