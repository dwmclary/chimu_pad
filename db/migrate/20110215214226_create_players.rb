class CreatePlayers < ActiveRecord::Migration
  def self.up
    create_table :players do |t|
      t.string :name,   :null => false
      t.integer :number,  :null => false
      t.integer :team_id, :null => false
      t.string :position, :null => false
      t.string :team, :null => false
      t.string :comment
      t.float :current_rating

      t.timestamps
    end
  end

  def self.down
    drop_table :players
  end
end
