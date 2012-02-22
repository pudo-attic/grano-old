var grano = grano || {};

grano.Network = Backbone.Model.extend({
    idAttribute: "slug"
});
 
grano.NetworkCollection = Backbone.Collection.extend({
    model: grano.Network,
    url: "/api/1/networks"
});

grano.NetworkListView = Backbone.View.extend({
    el: $('#network-list'),
    initialize: function() {
        this.model.bind("reset", this.render, this);
    },
    render: function(eventName) {
        _.each(this.model.models, function(network) {
            $(this.el).append(
                new grano.NetworkListItemView({model: network}).render().el);
        }, this);
        return this;
    }
});
 
grano.NetworkListItemView = Backbone.View.extend({
    tagName: "li",
    template: _.template($('#network-list-item').html()),
    render: function(eventName) {
        $(this.el).html(this.template(this.model.toJSON()));
        return this;
    }
});

var AppRouter = Backbone.Router.extend({
    routes: {
        ""               : "list",
        "networks/:slug" : "networkDetails"
    },
 
    list: function() {
        console.log('list');
        this.networkList = new grano.NetworkCollection();
        this.networkListView = new grano.NetworkListView({model: this.networkList});
        this.networkList.fetch();
    },
 
    networkDetails: function(slug) {
        this.network = this.networkList.get(slug);
        this.networkView = new grano.NetworkView({model: this.wine});
        this.networkView.render();
    }
});
 
var app = new AppRouter();
Backbone.history.start();
