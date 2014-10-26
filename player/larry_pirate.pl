#!/usr/bin/perl
#
# Larry The Pirate
#
use warnings;
use strict;
use Data::Dumper;
use Dancer;

use List::Util qw(max);

set 'logger'       => 'console';
set 'show_errors'  => 1;
set 'startup_info' => 1;
set 'warnings'     => 1;

get '/ping' => sub {
    return "pong\n";
};

post '/bid' => sub {
    debug "--- NEW BID ---";
    my $data = from_json(request->body);

    my $players = $data->{players};
    my $gameplay = $data->{gameplay};
    my $dice = $data->{dice};

    my $players_count = scalar @$players;
    debug "players_count: $players_count";

    my $players_dice_count;
    $players_dice_count += $_->{dice} for @$players;
    debug "players_dice_count: $players_dice_count";

    my $last_move = $gameplay->[-1] || q[];

    # We start the game
    if (!$last_move) {
        my $next_bid_count = $players_dice_count/$players_count + 1;
        my $next_bid_dice = max(@$dice);
        debug "next_bid_dice: $next_bid_dice";
        debug "We start the game";

        my $bid = [ $next_bid_count, $next_bid_dice ];
        debug "Returning" . join(', ', @$bid);

        return to_json($bid);
    }

    my ($last_bid_count, $last_bid_dice) = @$last_move[-2,-1];
    debug "last_bid_count: $last_bid_count";
    debug "last_bid_dice: $last_bid_dice";

    $last_bid_dice = $last_bid_dice || max(@$dice);

    my @tolerance_map = (-2, -1, 0, 1, 2, 3, 4);
    my $tolerance = $tolerance_map[rand @tolerance_map];
    my $max_bid_count = $players_dice_count/$players_count + $tolerance;
    debug "tolerance: $tolerance";
    debug "max_bid_count: $max_bid_count";

    # Make a call
    if ($last_bid_count >= $max_bid_count) {
        my $call = [ 0,0 ];
        debug "Returning " . join(', ', @$call);
        return to_json($call);
    }

    my @bid_count_add_map = (1,2,3);
    my $bid_count_add = $bid_count_add_map[rand @bid_count_add_map];

    my $next_bid_count = $last_bid_count + $bid_count_add;
    debug "bid_count_add: $bid_count_add";
    debug "next_bid_count: $next_bid_count";

    # Make a call
    if ($next_bid_count >= $players_dice_count) {
        my $call = [ 0,0 ];
        debug "Returning " . join(', ', @$call);
        return to_json($call);
    }

    my $next_bid_dice = @$gameplay % 2 ? max(@$dice) : $last_bid_dice;
    debug "next_bid_dice: $next_bid_dice";

    my $bid = [ $next_bid_count, $next_bid_dice ];
    debug "Returning " . join(', ', @$bid);

    return to_json($bid);
};

dance;
