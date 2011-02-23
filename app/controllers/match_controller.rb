class MatchController < ApplicationController
  
  def show
    @match = Match.find(params["id"])
    home_graph = Graph.where(:match_id => @match.id, :kind => "single", :team_id => @match.home_team_id)[0]
    away_graph = Graph.where(:match_id => @match.id, :kind => "single", :team_id => @match.away_team_id)[0]
    @home_team_name = Team.find(@match.home_team_id).name
    @away_team_name = Team.find(@match.away_team_id).name
    @home_nodes = home_graph.get_nodelist()
    @home_edges = home_graph.get_edgelist()
    @away_nodes = away_graph.get_nodelist()
    @away_edges = away_graph.get_edgelist()
    respond_to do |format|
      format.html
    end
  end
end
