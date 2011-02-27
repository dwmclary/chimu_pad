class LeagueController < ApplicationController
  
  def index
    respond_to do |format|
      format.html {redirect_to :action => "show", :id => params["id"]}
    end
  end
  
  def show
    @league = League.find(params["id"])
    @matches = Match.paginate :page => params[:page], :order => "match_date asc", :per_page => 10
    @teams = @league.teams.sort{|t1,t2|t2.current_rating <=> t1.current_rating}
    @team_columns = get_team_columns(@teams)
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
