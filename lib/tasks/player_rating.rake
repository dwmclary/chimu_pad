namespace :player do
  task :rating => :environment do  
    desc "Compute and save current player ratings"
    players = Player.all()
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
  end
end