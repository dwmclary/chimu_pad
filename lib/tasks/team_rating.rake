namespace :team do
  task :rating => :environment do  
    desc "Compute and save current team ratings for each league"
    leagues = League.all()
    leagues.each{|league|
      teams = league.teams
      matches = Team.where(:league_id => league.id).map{|t| t.match_count()}
      max_matches = matches.max
      teams.each{|t|
        # puts t.name
        match_ratings = t.match_ratings()
        if match_ratings.size() > 0:
          t.current_rating = t.performance
        else
          t.current_rating = 0.0
        end
        t.save()
      }
    }
  end
end