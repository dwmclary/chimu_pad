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
  
  def match_count
    home_matches = Match.count(:conditions => ["home_team_id = (?)",self.id])
    away_matches = Match.count(:conditions => ["away_team_id = (?)",self.id])
    return home_matches + away_matches
  end
  
  def average_rating
    match_ratings = self.match_ratings()
    # we need to find the maximum Match count for all teams
    matches = Team.all().map{|t| t.match_count()}
    max_matches = matches.max
    while match_ratings.size() < max_matches do
      match_ratings.push(0.0)
    end
    
    if match_ratings.size() > 0:
      self.current_rating = match_ratings.sum/max_matches
    else
      self.current_rating = 0.0
    end
  end
    
    
    
end
