namespace :player do
  task :rating => :environment do  
    desc "Compute and save current player ratings"
    players = Player.all()
    all_player_ratings = Player.all().map{|p| p.play_count()}
    max_ratings = all_player_ratings.max
    players.each{|p|
      puts p.name    
      ratings = p.ratings()
      while ratings.size < max_ratings do
        ratings.push(0.0)
      end
      p.current_rating = ratings.sum/max_ratings
      p.save()
    }
  end
end