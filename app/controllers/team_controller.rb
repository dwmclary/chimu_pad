class TeamController < ApplicationController
  
  def index
    teams = Team.where(:league_id => 1)
    teams.each{|team|
      team.average_rating()
    }
    teams.sort!{|t1,t2| t2.current_rating <=> t1.current_rating}
    @team_columns = get_team_columns(teams)
    respond_to do |format|
      format.html 
    end
  end
  
  def show
    @team = Team.find(params["id"])
    @team.average_rating()
    home_matches = Match.where(:home_team_id => @team.id)
    away_matches = Match.where(:away_team_id => @team.id)
    @matches = home_matches + away_matches
    @players = @team.players
    @players.sort!{|p1,p2| p2.current_rating <=> p1.current_rating}
    @matches.sort!{|m1,m2| m1.match_date <=> m2.match_date}
    @match_ratings = @team.match_ratings()
    @best_ratings = @players.first.ratings()
    worst_player = nil
    @players.reverse_each{|x|
      if x.ratings().size() > 0:
        worst_player = x
      end
    }
    @worst_ratings = worst_player.ratings()
    respond_to do |format|
      format.html
    end
  end
  
  def get_team_columns(team_list)
    #determine how many columns we want
    column_count = team_list.size()/10
    set = []
    count = 0
    (0..column_count-1).each{|i|
      column = []
      (0..10).each{|j|
        if team_list[count] != nil
          column.push(team_list[count])
          count += 1
        end
      }
      set.push(column)
    }
    return set
  end
  
end
