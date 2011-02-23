class Match < ActiveRecord::Base
  belongs_to :team
  has_many :graph
end
