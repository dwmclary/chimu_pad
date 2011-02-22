class CreateTeams < ActiveRecord::Migration
  def self.up
    create_table :teams do |t|
      t.string :name,   :null => false
      t.integer :league_id, :null => false
      t.string :country
      t.string :abbreviation
      t.float :current_rating

      t.timestamps
    end
  end

  def self.down
    drop_table :teams
  end
end
