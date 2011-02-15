class CreatePlayerRatings < ActiveRecord::Migration
  def self.up
    create_table :player_ratings do |t|
      t.integer :player_id
      t.float :rating
      t.timestamp :rating_date

      t.timestamps
    end
  end

  def self.down
    drop_table :player_ratings
  end
end
