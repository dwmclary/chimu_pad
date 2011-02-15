class CreateTeamRatings < ActiveRecord::Migration
  def self.up
    create_table :team_ratings do |t|
      t.integer :team_id
      t.float :rating
      t.timestamp :rating_date

      t.timestamps
    end
  end

  def self.down
    drop_table :team_ratings
  end
end
