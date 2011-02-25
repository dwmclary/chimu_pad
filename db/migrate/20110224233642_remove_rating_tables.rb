class RemoveRatingTables < ActiveRecord::Migration
  def self.up
    drop_table :player_ratings
    drop_table :team_ratings
    add_column :teams, :current_rating, :float
  end

  def self.down
    create_table :player_ratings do |t|
      t.integer :player_id, :null => false
      t.integer :match_id, :null => false
      t.float :rating
      t.datetime :rating_date

      t.timestamps
    end
    
    create_table :team_ratings do |t|
      t.integer :match_id, :null => false
      t.integer :team_id, :null => false
      t.float :rating
      t.datetime :rating_date

      t.timestamps
    end
    
    remove_column :teams, :current_rating
  end
end
