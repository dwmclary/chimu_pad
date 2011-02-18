class CreateMatches < ActiveRecord::Migration
  def self.up
    create_table :matches do |t|
      t.integer   :league_id, :null => false
      t.integer   :home_team_id, :null => false
      t.integer   :away_team_id, :null => false
      t.integer   :home_team_score, :null => false
      t.integer   :away_team_score, :null => false
      t.string    :location 
      t.integer   :winning_team_id
      t.datetime  :match_date

      t.timestamps
    end
  end

  def self.down
    drop_table :matches
  end
end
