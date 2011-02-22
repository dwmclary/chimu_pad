class TeamController < ApplicationController
  
  def index
    respond_to do |format|
      format.html {render :action => "show", :id => params["id"]}
    end
  end
  
  def show
    @team = Team.find(params["id"])
    @home_matches = Match.where(:home_team_id => @team.id)
    @away_matches = Match.where(:away_team_id => @team.id)
    respond_to do |format|
      format.html
    end
  end
  
end
