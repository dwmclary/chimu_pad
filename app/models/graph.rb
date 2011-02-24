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
        from = Player.find(from.to_i()).number
      end
      
      if not ignored_nodes.include? to
        to = Player.find(to.to_i()).number
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
        node_id = player.number
      end
      
      if size
        size = size.split(":")
        size = {"size" => size.last.to_f(), "color"=>set_color(size.last.to_f()), "x"=>x, "y"=>y}
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

    x = nil
    y = nil
    positions = []
    (50..275).step(50){|p| positions.push(p)}
    #if this is the home team, place the player on the left side
    if player.team_id == home_team_id
      if player.position == "GK"
        x = 50
        y=50
      elsif player.position == "DF"
        #choose a random y for this defender
        x = 100
        y= positions.choice()
      elsif player.position == "MF"
        x = 200
        y = positions.choice()
      elsif player.position == "FW"
        x = 300
        y = positions.choice()
      end
      return x,y
    elsif player.team_id == away_team_id
      if player.position == "GK"
        x = 750
        y=50
      elsif player.position == "DF"
        #choose a random y for this defender
        x = 700
        y= positions.choice()
      elsif player.position == "MF"
        x = 600
        y = positions.choice()
      elsif player.position == "FW"
        x = 500
        y = positions.choice()
      end
    end
    return [x,y]
  end
  
  def set_color(rating)
    colors = {0 => "#FFF00",1 => "#FFF00", 2 => "#FFFCC", 3 => "#FFEDA0",4=> "#FED976", 5=>"#FEB24C" ,6=> "#FD8D3C" ,7=> "#FC4E2A", 8=> "#E31A1C",9=>"#BD0026", 10=>"#800026"}
    return colors[rating.ceil()]
  end
end
