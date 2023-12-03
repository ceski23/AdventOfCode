open Core
module CubeSets = Map.Make (String)

type game_constraint = string * int

let parse_round line =
  List.fold
    (Re2.get_matches_exn (Re2.create_exn "(?P<count>\\d+) (?P<color>[a-z]+)") line)
    ~init:CubeSets.empty
    ~f:(fun acc m ->
      let count = Re2.Match.get_exn m ~sub:(`Name "count") |> Int.of_string in
      let color = Re2.Match.get_exn m ~sub:(`Name "color") in
      Map.update acc color ~f:(fun value ->
        match value with
        | Some value -> max count value
        | None -> count))
;;

let parse_game line =
  let matches =
    Re2.first_match_exn (Re2.create_exn "Game (?P<game_id>\\d+): (?P<cube_sets>.*)") line
  in
  let game_id = Re2.Match.get_exn matches ~sub:(`Name "game_id") |> Int.of_string in
  let cube_sets = Re2.Match.get_exn matches ~sub:(`Name "cube_sets") |> parse_round in
  game_id, cube_sets
;;

let is_game_possible (constraints : game_constraint list) (cube_sets : int CubeSets.t) =
  constraints
  |> List.for_all ~f:(fun (color, max_count) ->
    match Map.find cube_sets color with
    | Some count -> count <= max_count
    | None -> false)
;;

let sum_possible_game_ids acc line =
  let game_id, cube_sets = parse_game line in
  match is_game_possible [ "red", 12; "green", 13; "blue", 14 ] cube_sets with
  | true -> acc + game_id
  | false -> acc
;;

let () =
  let result =
    In_channel.with_file
      "days/day2/input.txt"
      ~f:(In_channel.fold_lines ~init:0 ~f:sum_possible_game_ids)
  in
  printf "PART1: %d\n" result;
  assert (result = 2879)
;;

let calc_set_power (cube_sets : int CubeSets.t) =
  Map.data cube_sets |> List.fold ~init:1 ~f:(fun acc count -> acc * count)
;;

let sum_set_powers acc line =
  let _, cube_sets = parse_game line in
  acc + calc_set_power cube_sets
;;

let () =
  let result =
    In_channel.with_file
      "days/day2/input.txt"
      ~f:(In_channel.fold_lines ~init:0 ~f:sum_set_powers)
  in
  printf "PART2: %d\n" result;
  assert (result = 65122)
;;
