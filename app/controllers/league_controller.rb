class LeagueController < ApplicationController
  
  def index
    respond_to do |format|
      format.html {redirect_to :action => "show", :id => params["id"]}
    end
  end
  
  def show
    @league = League.find(params["id"])
    respond_to do |format|
      format.html
    end
  end
end
