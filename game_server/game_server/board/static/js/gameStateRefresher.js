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

              //moving frame{
              var $currentPlayerInfo = $('<div class="col-md-6"></div>');
             $currentPlayerInfo.css({'border':'solid 2px transparent'});
              var extra_class = '';
              if (player.id === data.last_player){
                  extra_class = 'alert-danger';
//                 $currentPlayerInfo.css({'background-color:':'red', 'border-color': 'white'});
              } else {
//                  $currentPlayerInfo.css({'background-color:':'white', 'border-color':'white'});
              }

              //skip player only if was not banned in the last round
              if (player.active === false && player.id !== data.last_player){
                  continue;
              }

              // player avatar and name
              var $playerID = $('<div class="col-md-12 col-xs-12 nopadding"></div>');
              var $playerName = $('<div class="col-md-9 col-xs-9 " style="padding-top:5%"><b>' + player.name + '</b></div>');
              // add avatar only if exists
              var $playerAvatarImg = $('<img class="scaled avatar">');
//              if (player.avatar !== ''){
//                  $playerAvatarImg.attr({'src': player.avatar})
//              } else {
                  $playerAvatarImg.attr({"src": '/static/img/avatar-'+ player.name.toLowerCase() +'.png', "style":"margin-bottom: 1em"})
//              }

              var $playerAvatar = $('<div class="col-md-3 col-xs-3 nopadding" ></div>').append($playerAvatarImg);

              $playerID.append($playerAvatar);
              $playerID.append($playerName);
              $currentPlayerInfo.append($playerID);

              $('<div class="dice col-md-12 col-xs-12 badge badge-info '+ extra_class + '">Player\'s dice</div>').appendTo($currentPlayerInfo);
              var $diceDiv = $('<div class="col-md-12 col-xs-12 "></div>');

              var dice = player.dice;
              for(var die in dice){
                  var die = dice[die];
                  var $dieImgs = $('<img class="scaled">').attr({'src': '/static/img/'+die+'k6.png'});
                  $('<div class="col-md-2 col-xs-2  nopadding" style="overflow:hidden"></div>').append($dieImgs).appendTo($diceDiv);
              }
              $currentPlayerInfo.append($diceDiv);

              // player's bid
              $('<div class="dice col-md-12 col-xs-12 badge badge-info '+ extra_class+'" style="margin-top:1em" >Last bid</div>').appendTo($currentPlayerInfo);
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

                  //put empty block if somebody is calling
                  if (quantity ==0 && diceValue == 0){
                    var $dieImgs = $('<img class="scaled">')
                   .attr({'src': '/static/img/empty_image.png'});
                   $('<div class="col-md-2 col-xs-2 nopadding" style="overflow:hidden"></div>').append($dieImgs).appendTo($bidDiceDiv);
                  }
              } else{
                  // no bid, but we want an empty block to keep the layout
                   var $dieImgs = $('<img class="scaled">')
                   .attr({'src': '/static/img/empty_image.png'});
                   $('<div class="col-md-2 col-xs-2 nopadding" style="overflow:hidden"></div>').append($dieImgs).appendTo($bidDiceDiv);
              }
              $currentPlayerInfo.append($bidDiceDiv);
              // finally add rest
              $playersInfo.append($currentPlayerInfo);
          }
          var $messageBox = $('h1#messageText');
          $messageBox.html("&nbsp;"+data.message);

          if (data.the_end == true) iterationNumber=-1;
      });
    }

    setInterval(function() { if (iterationNumber ==-1){ return;}refreshGameState()}, 3000);