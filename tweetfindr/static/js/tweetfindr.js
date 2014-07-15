(function($){
  // Route to hit the API and return tweets
  var AppRouter = Backbone.Router.extend({
    routes: {
      'account/:id': 'displayTweets',
    },

    // Attempt to display the tweets based on the route information
    displayTweets: function (account_id) {
      var tweets = new TweetList();
      var tweetsView = new TweetView({collection: tweets});
      tweets.account_id = account_id;
      tweets.fetch({
        success: function(){
          tweetsView.render();
        },
        // If an error pops up, display it in a modal
        error: function(model, response){
          $('#error-message').append(response.responseText);
          $('#errorModal').modal({
            backdrop: true
          });
        }
      });
    }
  });

  var Tweet = Backbone.Model.extend({
    idAttribute: "id"
  });

  // Collection
  var TweetList = Backbone.Collection.extend({
    model: Tweet,

    url: function() {
      return '/account/' + this.account_id;
    }
  });

  // View, which appends to the #append-tweets div using the #tweetTemplate template
  var TweetView = Backbone.View.extend({
    el: "#append-tweets",

    events: {
      'click .tweet-reply': 'tweetReply',
    },

    tweetReply: function(evt) {
      var tweetId = $(evt.target).attr('data-target');
        var this_tweet = this.collection.find(function(model) { return model.get('tweet_id') == tweetId; });
        alert('Original tweet by ' + this_tweet.get('username') + ': ' + this_tweet.get('text') + '\n\nTweet ID: ' + this_tweet.get('tweet_id') + '\n\nUser ID: ' + this_tweet.get('user_id'));
    },

    template: _.template($('#tweetTemplate').html()),

    render: function(eventName) {
    _.each(this.collection.models, function(tweet){
      var tweetTemplate = this.template(tweet.toJSON());
        $(this.el).append(tweetTemplate);
        }, this);
      return this;
    }
  });

  // On page load, set it up so if an ajax call happens, display the loader
  $(document).ajaxStart(function(){
      $('#loading').show();
   }).ajaxStop(function(){
      $('#loading').hide();
   });

  // Instantiate the Backbone app
  var app_router = new AppRouter;

  Backbone.history.start();
})(jQuery);
