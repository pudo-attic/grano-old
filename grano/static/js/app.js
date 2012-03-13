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

my.applyValidationErrors = function($el, resp) {
  var data = JSON.parse(resp.responseText);
  for (var field in data.errors) {
    var elem = field.split('.', 2)[1];
    var el = $($el).find("*[id='" + elem + "']");
    el.parents(".control-group").addClass("error");
    el.after("<span class='help-inline'>" + data.errors[field] + "</span>");
  }
};

my.Models.Network = Backbone.Model.extend({
  idAttribute: 'slug',
  url : function() {
    if (this.isNew()) 
      return my.Config.ApiEndpoint + 'networks';
    return my.Config.ApiEndpoint + this.id;
  }
});

my.Collections.Networks = Backbone.Collection.extend({
  model: my.Models.Network,
  initialize: function() {},
  url : function() {
    return my.Config.ApiEndpoint + 'networks';
  }
});

my.Views.Network = Backbone.View.extend({
  events: {
    "click #edit-network": "edit"
  },

  template: Handlebars.compile($("#network-view").html()),

  initialize: function() {
    this.render();
  },

  edit: function() {
    window.app.navigate(this.model.id + "/edit", {trigger: true});
  },

  render: function() {
    var html = this.template(this.model.toJSON());
    $(this.el).html(html);
    $('#app').html(this.el);
  }  

});

my.Views.NetworkEdit = Backbone.View.extend({
  events: {
      "submit form": "save"
  },

  template: Handlebars.compile($("#network-edit").html()),
    
  initialize: function() {
    this.render();
  },

  save: function() {
    var self = this;
    var data = $(this.el).find("form").serializeObject();
    if (!this.model.isNew()) {
      data.slug = this.model.id;
    }
    this.model.save(data, {
      success: function(model, resp) {
        window.app.networksView.update();
        window.app.navigate(model.id, {trigger: true});
      },
      error: function(model, resp) {
        my.applyValidationErrors(self.el, resp);
      }
    });
    return false;
  },
  
  render: function() {
    var data = this.model.toJSON();
    data.heading = this.model.isNew() ? 'Make a network' : data.title;
    var html = this.template(data);
    $(this.el).html(html);
    $('#app').html(this.el);
  }  

});

my.Views.NetworkList = Backbone.View.extend({

  template: Handlebars.compile($("#network-list").html()),

  initialize: function() {
  },

  update: function() {
    var self = this;
    this.model.fetch({
      success: function() {
        self.render();
      }
    });
  },

  render: function() {
    var data = {networks: this.model.toJSON()};
    var html = this.template(data);
    $(this.el).html(html);
    $('#network-list-elem').html(this.el);
  }  

});

my.App = Backbone.Router.extend({

  routes: {
    "newNetwork":  "newNetwork",
    ":slug":        "viewNetwork",
    ":slug/edit":   "editNetwork"
  },

  initialize: function(options) {
    my.Config.ApiEndpoint = '/api/1/';
    this.listNetworks();  
  },

  listNetworks: function() {
    var self = this;
    this.networks = new my.Collections.Networks();
    this.networksView = new my.Views.NetworkList({model: this.networks});
    this.networksView.update();
  },

  newNetwork: function() {
    new my.Views.NetworkEdit({ model: new my.Models.Network() });
  },

  editNetwork: function(slug) {
    var model = new my.Models.Network({slug: slug});
    model.fetch({
      success: function(model) {
        new my.Views.NetworkEdit({ model: model });
      }
    }); 
  },

  viewNetwork: function(slug) {
    var model = new my.Models.Network({slug: slug});
    model.fetch({
      success: function(model) {
        new my.Views.Network({ model: model });
      }
    });
  }

});

}(jQuery, this.Grano));