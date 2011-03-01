namespace :player do
  task :rating => :environment do  
    desc "Compute and save current player ratings"
    #for each league
    leagues = League.all()
    leagues.each{|league|
      #get the team ids
      team_ids = Team.where(:league_id => league.id).map(&:id)
      #get the players for the league
      players = Player.all(:conditions => ["team_id IN (?)", team_ids])
      players.each{|p|
        # puts p.name    
        all_player_ratings = Player.where(:team_id => p.team_id).map{|op| op.play_count()}
        max_ratings = all_player_ratings.max
        ratings = p.ratings()
        if ratings.size > 0:
          p.current_rating = ratings.sum/max_ratings
        else
          p.current_rating = 0.0
        end
        p.save()
      }
    }
  end
end