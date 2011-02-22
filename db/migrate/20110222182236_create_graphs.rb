class CreateGraphs < ActiveRecord::Migration
  def self.up
    create_table :graphs do |t|
      t.integer :match_id
      t.integer :team_id
      t.string :kind
      t.string :nodes
      t.string :edges

      t.timestamps
    end
  end

  def self.down
    drop_table :graphs
  end
end
