class Player < ActiveRecord::Base
  # belongs_to :team
  public
  
  def average_rating
    ratings = Play.where(:player_id => self.id).map(&:rating)
    if ratings.size() > 0:
      #get the counts for all players
      all_player_ratings = Player.all().map{|p| p.play_count()}
      max_ratings = all_player_ratings.max
      while ratings.size < max_ratings do
        ratings.push(0.0)
      end
      self.current_rating = ratings.sum/max_ratings
      return ratings.sum/max_ratings
    else
      return 0.0
    end
  end
  
  def play_count
    plays = Play.count(:conditions => ["player_id = (?)", self.id])
    return plays
  end
  
  def ratings
    ratings = Play.where(:player_id => self.id).map(&:rating)
    return ratings
  end
end
