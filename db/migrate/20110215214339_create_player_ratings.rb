class CreatePlayerRatings < ActiveRecord::Migration
  def self.up
    create_table :player_ratings do |t|
      t.integer :player_id, :null => false
      t.integer :match_id, :null => false
      t.float :rating
      t.datetime :rating_date

      t.timestamps
    end
  end

  def self.down
    drop_table :player_ratings
  end
end
