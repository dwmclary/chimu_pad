namespace :team do
  task :rating => :environment do  
    desc "Compute and save current team ratings"
    teams = Team.all()
    matches = Team.all().map{|t| t.match_count()}
    max_matches = matches.max
    teams.each{|t|
      puts t.name
      match_ratings = t.match_ratings()
      while match_ratings.size() < max_matches do
        match_ratings.push(0.0)
      end
      if match_ratings.size() > 0:
        t.current_rating = match_ratings.sum/max_matches
      else
        t.current_rating = 0.0
      end
      t.save()
    }
  end
end