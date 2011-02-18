class TeamController < ApplicationController
  
  def index
    t_id = params["id"]
    @players = Player.where(:team_id => t_id)
    respond_to do |format|
      format.html #index.html.erb
      format.xml { render :xml => @teams}
    end
  end
end
