SELECT name, height, main_position, ps.season, ps.squad, ps.goals, pt.MV, pt.transfer_Fee FROM player
JOIN player_statistics ps on player.id = ps.player_id
JOIN player_transfers pt on player.id = pt.player_id AND ps.season = pt.season AND ps.club_id = pt.joined
WHERE pt.transfer_Fee != 0 and pt.MV != 0;