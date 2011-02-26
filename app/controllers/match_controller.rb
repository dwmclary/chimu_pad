class MatchController < ApplicationController
  
  def show
    @match = Match.find(params["id"])
    dualgraph = Graph.where(:match_id => @match.id, :kind => "double")[0]

    @home_team_name = Team.find(@match.home_team_id).name
    @away_team_name = Team.find(@match.away_team_id).name
    home_players = Player.find_all_by_team_id(@match.home_team_id, :select=>:id)
    away_players = Player.find_all_by_team_id(@match.away_team_id, :select => :id)
    hp_ids = home_players.map(&:id)
    aw_ids = away_players.map(&:id)
    @home_plays = Play.all(:conditions => ["match_id = (?) AND player_id IN (?)", @match.id, hp_ids])
    puts @home_plays.size()
    @home_plays.sort!{|m1,m2| m2.rating <=> m1.rating}
    @away_plays = Play.all(:conditions => ["match_id = (?) AND player_id IN (?)", @match.id, aw_ids])
    @away_plays.sort!{|m1,m2| m2.rating <=> m1.rating}
    @nodes = dualgraph.get_nodelist()
    @edges = dualgraph.get_edgelist()
    respond_to do |format|
      format.html
    end
  end
end
