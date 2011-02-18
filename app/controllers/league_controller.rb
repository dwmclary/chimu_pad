class LeagueController < ApplicationController
  
  def index
    league_id = params["id"]
    @teams = Team.where(:league_id => league_id)
    respond_to do |format|
      format.html #index.html.erb
      format.xml { render :xml => @teams}
    end
  end
end
