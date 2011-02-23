class LeagueController < ApplicationController
  
  def index
    respond_to do |format|
      format.html {redirect_to :action => "show", :id => params["id"]}
    end
  end
  
  def show
    @league = League.find(params["id"])
    @league.matches.sort!{|m1,m2| m1.match_date <=> m2.match_date}
    respond_to do |format|
      format.html
    end
  end
end
