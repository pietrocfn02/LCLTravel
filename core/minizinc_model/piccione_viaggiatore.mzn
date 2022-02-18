include "alldifferent.mzn";

%input
int: n;

set of int: central = 2..n;

% input
array[1..n,1..n] of int: dist;
% input
int: start_city;

% input
array[1..n] of string: city_names;

% variabile decisionale
array[1..n+1] of var 1..n+1:city;

%%%%%%%%%%%%constraints %%%%%%%%%%%%%
constraint city[1] = start_city;
constraint city[n+1] = start_city;


constraint forall(i in central, j in central)(if (i!=j) then city[i] != city[j] endif);

constraint forall(i in central)(city[i] != start_city);

var int: total_distance = sum (i in 1..n)(dist[city[i],city[i+1]]);
%array[1..n] of var string : visited;
%constraint forall (i in 1..n)(visited[i] = city_names[city[i]]);
solve minimize total_distance;

output [city_names[fix(city[1])]]++["\n"++city_names[fix(city[i])]| i in 2..n+1] ++
["\nDistanza percorsa ", show(total_distance)];