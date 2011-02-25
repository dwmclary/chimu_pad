class Team < ActiveRecord::Base
  belongs_to :league
  has_many :players
  
  def match_ratings
    #get the set of all matches
    home_matches = Match.where(:home_team_id => self.id)
    away_matches = Match.where(:away_team_id => self.id)
    all_matches = home_matches + away_matches
    all_matches.sort!{|m1,m2| m1.match_date <=> m2.match_date}
    #get the set of player ids
    player_ids = self.players.map(&:id)
    all_ratings = []
    #for each match, get the plays for all players
    all_matches.each{|m|
      plays = Play.all(:conditions => ["match_id = (?) AND player_id IN (?)", m.id, player_ids])
      ratings = plays.map(&:rating)
      if ratings.size() > 0:
        all_ratings.push(ratings.sum/ratings.size())
      else
        all_ratings.push(0.0)
      end
    }
    return all_ratings
  end
  
  def average_rating
    match_ratings = self.match_ratings()
    rating = 0.0
    if match_ratings.size() > 0:
      self.current_rating = match_ratings.sum/match_ratings.size()
    end
  end
    
    
    
end
