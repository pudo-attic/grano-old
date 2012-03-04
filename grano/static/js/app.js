// # Grano Backbone Models
this.Grano = this.Grano || {};
this.Grano.Config = this.Grano.Config || {};
this.Grano.Models = this.Grano.Models || {};
this.Grano.Collections = this.Grano.Collections || {};
this.Grano.Views = this.Grano.Views || {};

(function($, my) {

$.fn.serializeObject = function() {
  var o = {};
  var a = this.serializeArray();
  $.each(a, function() {
      if (o[this.name] !== undefined) {
          if (!o[this.name].push) {
              o[this.name] = [o[this.name]];
          }
          o[this.name].push(this.value || '');
      } else {
          o[this.name] = this.value || '';
      }
  });
  return o;
};

my.Models.Network = Backbone.Model.extend({
  idAttribute: 'slug',
  url : function() {
    if (this.isNew()) 
      return my.Config.ApiEndpoint + 'networks';
    return my.Config.ApiEndpoint + this.id;
  }
});


my.Views.NetworkEdit = Backbone.View.extend({
  events: {
      "submit form": "save"
  },
    
  initialize: function() {
    this.template = Handlebars.compile($("#network-edit").html());
    this.render();
  },

  save: function() {
    var data = $(this.el).find("form").serializeObject();
    console.log(data);
    this.model.save(data, {
      success: function(model, resp) {},
      error: function(model, resp) {
        console.log(resp);
      }
    });
    return false;
  },
  
  render: function() {
    var html = this.template(this.model.toJSON());
    $(this.el).html(html);
    $('#app').html(this.el);
  }  

});

my.App = Backbone.Router.extend({

  routes: {
    "networks":              "listNetworks",
    "networks/new":          "newNetwork",
    "networks/:slug":        "viewNetwork"
  },

  initialize: function(options) {
    my.Config.ApiEndpoint = '/api/1/';
  },

  listNetworks: function() {
    console.log("Banana!");
  },

  newNetwork: function() {
    new my.Views.NetworkEdit({ model: new my.Models.Network() });
  },

  viewNetwork: function(slug) {
    
  }

});

}(jQuery, this.Grano));