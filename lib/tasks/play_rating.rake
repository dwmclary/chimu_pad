namespace :play do
  task :rating => :environment do
    desc "Read updated ratings from match graphs and propagate to Play objects"
    #get all the double graphs
    g = Graph.where(:kind => "double")
    #for each double graph
    g.each{|graph|
      #find all the plays related to it
      plays = Play.where(:match_id => graph.match_id)
      #get the hash of node ratings
      nodes = graph.get_node_ids
      #update each play
      plays.each{|p|
        puts nodes[p.player_id]
        p.rating = nodes[p.player_id]
        p.save
      }
   }
  end
end