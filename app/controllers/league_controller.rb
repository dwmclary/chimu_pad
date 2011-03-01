class LeagueController < ApplicationController
  
  def index
    respond_to do |format|
      format.html {redirect_to :action => "show", :id => params["id"]}
    end
  end
  
  def show
    @league = League.find(params["id"])
    @teams = @league.teams.sort{|t1,t2|t2.current_rating <=> t1.current_rating}
    @rankings = (1..@teams.size).to_a()
    team_ids = @teams.map(&:id)
    @matches = Match.paginate :page => params[:page], :order => "match_date asc", :conditions=> ["home_team_id IN (?)", team_ids], :per_page => 10
    @players = Player.paginate :page => params[:playerpage], :order => "current_rating desc", :conditions=> ["team_id IN (?)", team_ids], :per_page => 6

    @team_columns = get_columns(@teams,10)
    respond_to do |format|
      format.html
    end
  end
  
  def get_columns(item_list,divisor)
    #determine how many columns we want
    column_count = item_list.size()/divisor
    set = []
    count = 0
    (0..column_count-1).each{|i|
      column = []
      (0..10).each{|j|
        if item_list[count] != nil
          column.push(item_list[count])
          count += 1
        end
      }
      set.push(column)
    }
    return set
  end
  
end
