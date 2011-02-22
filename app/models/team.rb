class Team < ActiveRecord::Base
  belongs_to :league
  has_many :players
  has_many :matches
end
