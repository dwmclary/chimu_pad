class Player < ActiveRecord::Base
  # belongs_to :team
  public
  
  def average_rating
    ratings = Play.where(:player_id => self.id).map(&:rating)
    if ratings.size() > 0:
      self.current_rating = ratings.sum/ratings.size()
      self.save()
      return ratings.sum/ratings.size()
    else
      return 0.0
    end
  end
  
  def ratings
    ratings = Play.where(:player_id => self.id).map(&:rating)
    return ratings
  end
end
