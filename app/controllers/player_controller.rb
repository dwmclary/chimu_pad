class PlayerController < ApplicationController
  
  def index
    @players = Player.paginate :page => params[:playerpage], :order => "current_rating desc", :per_page => 7
    respond_to do |format|
      format.html
    end
  end
  
  def show
    @player = Player.find(params["id"])
    @plays = Play.find_all_by_player_id(@player.id)
    @plays.sort!{|p1,p2| p1.match.match_date <=> p2.match.match_date}
    ratings = @plays.map(&:rating)
    @opponents = []
    @plays.each{|p|
      #if we were the home team, get the away team
      if p.match.home_team_id == @player.team_id
        @opponents.push(Team.find(p.match.away_team_id, :select => :name).name)
      else
        @opponents.push(Team.find(p.match.home_team_id, :select => :name).name)
      end
    }
    @rating_data = []
    ratings.each_with_index{|r,i|
      @rating_data.push(r)
    }
    @team = Team.find(@player.team_id)
    @average_ratings = @team.match_ratings()
    respond_to do |format|
      format.html
    end   
  end
end
