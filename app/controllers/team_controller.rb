class TeamController < ApplicationController
  
  def index
    respond_to do |format|
      format.html {render :action => "show", :id => params["id"]}
    end
  end
  
  def show
    @team = Team.find(params["id"])
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
  
end
