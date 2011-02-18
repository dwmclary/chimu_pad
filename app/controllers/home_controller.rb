require 'league'
class HomeController < ApplicationController
  def index
    @leagues = League.all()
    respond_to do |format|
      format.html #index.html.erb
      format.xml { render :xml => @leagues}
    end
  end

end
