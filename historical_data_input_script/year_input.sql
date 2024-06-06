use f1;

delimiter #
create procedure year_input()
begin

declare v_max int unsigned default 2024;
declare v_counter int unsigned default 1950;

  start transaction;
  while v_counter < v_max do
    INSERT INTO Seasons(season_year) VALUES (v_counter);
    set v_counter=v_counter+1;
  end while;
  commit;
end #

delimiter ;

call year_input();

DROP procedure year_input;
