# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# Note that this schema.rb definition is the authoritative source for your
# database schema. If you need to create the application database on another
# system, you should be using db:schema:load, not running all the migrations
# from scratch. The latter is a flawed and unsustainable approach (the more migrations
# you'll amass, the slower it'll run and the greater likelihood for issues).
#
# It's strongly recommended to check this file into your version control system.

ActiveRecord::Schema.define(:version => 20110222182236) do

  create_table "graphs", :force => true do |t|
    t.integer  "match_id"
    t.integer  "team_id"
    t.string   "kind"
    t.string   "nodes"
    t.string   "edges"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "leagues", :force => true do |t|
    t.string   "name",       :null => false
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "matches", :force => true do |t|
    t.integer  "league_id",       :null => false
    t.integer  "home_team_id",    :null => false
    t.integer  "away_team_id",    :null => false
    t.integer  "home_team_score", :null => false
    t.integer  "away_team_score", :null => false
    t.string   "location"
    t.integer  "winning_team_id"
    t.datetime "match_date"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "player_ratings", :force => true do |t|
    t.integer  "player_id",   :null => false
    t.integer  "match_id",    :null => false
    t.float    "rating"
    t.datetime "rating_date"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "players", :force => true do |t|
    t.string   "name",           :null => false
    t.integer  "number",         :null => false
    t.integer  "team_id",        :null => false
    t.string   "position",       :null => false
    t.string   "comment"
    t.float    "current_rating"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "plays", :force => true do |t|
    t.integer  "match_id",         :null => false
    t.integer  "player_id",        :null => false
    t.string   "position"
    t.integer  "shots"
    t.integer  "goals"
    t.integer  "passes_attempted"
    t.integer  "passes_completed"
    t.float    "rating"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "team_ratings", :force => true do |t|
    t.integer  "match_id",    :null => false
    t.integer  "team_id",     :null => false
    t.float    "rating"
    t.datetime "rating_date"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "teams", :force => true do |t|
    t.string   "name",           :null => false
    t.integer  "league_id",      :null => false
    t.string   "country"
    t.string   "abbreviation"
    t.float    "current_rating"
    t.datetime "created_at"
    t.datetime "updated_at"
  end

end
