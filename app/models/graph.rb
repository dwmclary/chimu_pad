require "player"

class Graph < ActiveRecord::Base
  belongs_to :match  
  
  def get_edgelist
    ignored_nodes = ["lost", "shots_on_goal", "shots_wide"]
    edgelist = []
    edges = self.edges.split(",")
    edges.each{|edge|
      from,to,weight = edge.split()
      if not ignored_nodes.include? from
        from = Player.find(from.to_i())
        from = from.team+from.number.to_s()
      end
      
      if not ignored_nodes.include? to
        to = Player.find(to.to_i())
        to = to.team+to.number.to_s()
      end
      
      if weight
        weight = {"weight" => weight.split(":").last.to_f()}
      else
        weight = {"weight" => 1.0}
      end
      
      edgelist.push([from,to,weight])
    }
    return edgelist
  end
  
  def get_node_ids
    ignored_nodes = ["lost", "shots_on_goal", "shots_wide"]
    nodes = {}
    nodelist = self.nodes.split(",")
    nodelist.each{|node|
      node_id, size = node.split()
      if not ignored_nodes.include? node_id
        if size
          size = size.split(":").last.to_f()
          nodes[node_id.to_i()] = size
        end
      end
    }
    return nodes
  end
  
  def get_nodelist
    ignored_nodes = ["lost", "shots_on_goal", "shots_wide"]
    nodelist = []
    nodes = self.nodes.split(",")
    nodes.each{|node|
      node_id, size = node.split()
      if not ignored_nodes.include? node_id
        player = Player.find(node_id.to_i())
        p = get_position(player)
        x = p.first
        y = p.last
        node_id = player.team + player.number.to_s()
      end
      
      if size and not ignored_nodes.include? node_id
        size = size.split(":")
        if size.last.to_f() > 0
          size = {"size" => size.last.to_f(), "color"=>set_color(size.last.to_f()), "x"=>x, "y"=>y}
        else
          size = {"size" => 5.0, "color"=>"FFFFE5", "x"=>x, "y"=>y}
        end
      else
        size = {"size" => 5.0, "color"=>"43A2CA"}
      end
      
      nodelist.push([node_id, size])
    }
    return nodelist
  end
  
  private
  
  def get_position(player)
    #find the home and away teams for this match
    match = Match.find(self.match_id)
    home_team_id = match.home_team_id
    away_team_id = match.away_team_id
    goalies = ["GK", "GC"]
    defenders = ["DF", "DR", "DC", "DL"]
    midfield = ["MF", "MR", "MC", "ML", "MD"]
    forwards = ["FW", "FL", "FR", "FC"]
    x = nil
    y = nil
    positions = []
    (50..275).step(50){|p| positions.push(p)}
    #if this is the home team, place the player on the left side
    if player.team_id == home_team_id
      if goalies.include? player.position
        x = 50
        y=50
      elsif defenders.include? player.position
        #choose a random y for this defender
        x = 100
        y= positions.choice()
      elsif midfield.include? player.position
        x = 200
        y = positions.choice()
      elsif forwards.include? player.position
        x = 300
        y = positions.choice()
      end
      return x,y
    elsif player.team_id == away_team_id
      if goalies.include? player.position
        x = 750
        y=50
      elsif defenders.include? player.position
        #choose a random y for this defender
        x = 700
        y= positions.choice()
      elsif midfield.include? player.position
        x = 600
        y = positions.choice()
      elsif forwards.include? player.position
        x = 500
        y = positions.choice()
      end
    end
    return [x,y]
  end
  
  def set_color(rating)
    colors = {0 => "FFFAA",1 => "FFFBB", 2 => "FFFCC", 3 => "FFEDA0",4=> "FED976", 5=>"FEB24C" ,6=> "FD8D3C" ,7=> "FC4E2A", 8=> "E31A1C",9=>"BD0026", 10=>"800026"}
    return colors[rating.floor()]
  end
end
