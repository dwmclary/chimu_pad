class CreateTeamRatings < ActiveRecord::Migration
  def self.up
    create_table :team_ratings do |t|
      t.integer :match_id, :null => false
      t.integer :team_id, :null => false
      t.float :rating
      t.datetime :rating_date

      t.timestamps
    end
  end

  def self.down
    drop_table :team_ratings
  end
end
