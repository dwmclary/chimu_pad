class TeamController < ApplicationController
  
  def index
    @teams = Team.where(:league_id => 1)
    @teams.sort!{|t1,t2| t2.current_rating <=> t1.current_rating}
    @team_ratings = @teams.map(&:current_rating)
    @team_columns = get_team_columns(@teams)
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
    play_counts = @players.map{|p| p.play_count()}
    max_plays = play_counts.max
    @best_players = []
    @players.each{|p|
      if p.play_count() == max_plays
        @best_players.push(p)
      end
    }
    @best_players.sort!{|p1,p2| p2.current_rating <=> p1.current_rating}
    @matches.sort!{|m1,m2| m1.match_date <=> m2.match_date}
    @players.sort!{|p1,p2| p2.current_rating <=> p1.current_rating}
    @match_ratings = @team.match_ratings()
    @best_ratings = @best_players.first.ratings()
    @worst_ratings = @best_players.last.ratings()
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
