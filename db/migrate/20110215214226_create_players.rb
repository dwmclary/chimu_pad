class CreatePlayers < ActiveRecord::Migration
  def self.up
    create_table :players do |t|
      t.string :name
      t.integer :number
      t.integer :team_id
      t.string :position
      t.float :current_rating

      t.timestamps
    end
  end

  def self.down
    drop_table :players
  end
end
