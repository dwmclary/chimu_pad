namespace :player do
  task :rating => :environment do  
    desc "Compute and save current player ratings"
    players = Player.all()
    all_player_ratings = Player.all().map{|p| p.play_count()}
    max_ratings = all_player_ratings.max
    players.each{|p|
      puts p.name    
      ratings = p.ratings()
      if ratings.size > 0:
        p.current_rating = ratings.sum/ratings.size
      else
        p.current_rating = 0.0
      end
      p.save()
    }
  end
end