   var iterationNumber = 0;
    var refreshGameState = function(){
      $.ajax('http://127.0.0.1:8000/board_state/' + iterationNumber + '/').done(function(data){
          //console.debug(data);
          iterationNumber++;

          data = $.parseJSON(data);
          //console.debug(data)

          // build div with players info
          var $playersInfo = $('#players_info').empty();
          //console.debug(data['players']);
          for(var j in data.players){
              var player = data.players[j];

              //skip players that were banned
              if (player.active == false){
                  continue;
              }

               //moving frame
              var $currentPlayerInfo = $('<div class="col-md-6"></div>');
              if (player.id === data.last_player){
                 $currentPlayerInfo.css({'border':'solid red'});
              }
              console.log($currentPlayerInfo);

              // player avatar and name
              var $playerID = $('<div class="col-md-12 col-xs-12 nopadding"></div>');
              var $playerName = $('<div class="col-md-9 col-xs-9 " style="padding-top:5%"><b>' + player.name + '</b></div>');
              // add avatar only if exists
              var $playerAvatarImg = $('<img class="scaled">');
              if (player.avatar !== ''){
                  $playerAvatarImg.attr({'src': player.avatar})
              } else {
                  $playerAvatarImg.attr({"src": '/static/img/avatar-blank.jpg', "style":"margin-bottom: 1em"})
              }

              var $playerAvatar = $('<div class="col-md-3 col-xs-3 nopadding" ></div>').append($playerAvatarImg);

              $playerID.append($playerAvatar);
              $playerID.append($playerName);
              $currentPlayerInfo.append($playerID);

              $('<div class="col-md-12 col-xs-12 badge badge-info">Player\'s dice</div>').appendTo($currentPlayerInfo);
              var $diceDiv = $('<div class="col-md-12 col-xs-12 "></div>');

              var dice = player.dice;
              for(var die in dice){
                  var die = dice[die];
                  var $dieImgs = $('<img class="scaled">').attr({'src': '/static/img/'+die+'k6.png'});
                  $('<div class="col-md-2 col-xs-2  nopadding" style="overflow:hidden"></div>').append($dieImgs).appendTo($diceDiv);
              }
              $currentPlayerInfo.append($diceDiv);

              // player's bid
              $('<div class="col-md-12 col-xs-12 badge badge-info" style="margin-top:1em" >Last bid</div>').appendTo($currentPlayerInfo);
              var $bidDiceDiv = $('<div class="col-md-12 col-xs-12 " ></div>');
              var bid = player.bid;


              if (bid.length == 2) {
                  var quantity = bid[0];
                  var diceValue = bid[1];

                  for (var i = 0; i < quantity; i++) {
                      var $dieImgs = $('<img class="scaled">')
                          .attr({'src': '/static/img/' + diceValue + 'k6.png'});

                      $('<div class="col-md-2 col-xs-2 nopadding" style="overflow:hidden"></div>').append($dieImgs).appendTo($bidDiceDiv);
                  }
                  $currentPlayerInfo.append($bidDiceDiv);
              }
              // finally add rest
              $playersInfo.append($currentPlayerInfo);
          }
          var $messageBox = $('h1#messageText');
          $messageBox.html(data.message);
      });
    }

    setInterval(function() {refreshGameState()}, 4000);
