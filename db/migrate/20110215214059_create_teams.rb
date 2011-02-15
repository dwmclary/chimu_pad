class CreateTeams < ActiveRecord::Migration
  def self.up
    create_table :teams do |t|
      t.string :name
      t.integer :league_id
      t.string :country
      t.float :current_rating

      t.timestamps
    end
  end

  def self.down
    drop_table :teams
  end
end
