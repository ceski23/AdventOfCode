open Core

module IntPairs = struct
  type t = int * int

  let compare (x0, y0) (x1, y1) =
    match compare x0 x1 with
    | 0 -> compare y0 y1
    | c -> c
  ;;

  let sexp_of_t = Tuple2.sexp_of_t Int.sexp_of_t Int.sexp_of_t
  let t_of_sexp = Tuple2.t_of_sexp Int.t_of_sexp Int.t_of_sexp
end

module PipesMap = Map.Make (IntPairs)

let point_from_index index width =
  let y = float index /. (width |> float) |> Float.round_down |> Int.of_float in
  let x = index mod width in
  y, x
;;

type side =
  | Left
  | Right
  | Top
  | Bottom

let left_pipes = [ '-'; 'L'; 'F' ]
let right_pipes = [ '-'; 'J'; '7' ]
let top_pipes = [ '|'; '7'; 'F' ]
let bottom_pipes = [ '|'; 'L'; 'J' ]

let is_valid_pipe pipe (side : side) reference =
  match side with
  | Left ->
    (if Char.( = ) reference 'S'
     then true
     else List.mem right_pipes reference ~equal:Char.( = ))
    && List.mem left_pipes pipe ~equal:Char.( = )
  | Right ->
    (if Char.( = ) reference 'S'
     then true
     else List.mem left_pipes reference ~equal:Char.( = ))
    && List.mem right_pipes pipe ~equal:Char.( = )
  | Top ->
    (if Char.( = ) reference 'S'
     then true
     else List.mem bottom_pipes reference ~equal:Char.( = ))
    && List.mem top_pipes pipe ~equal:Char.( = )
  | Bottom ->
    (if Char.( = ) reference 'S'
     then true
     else List.mem top_pipes reference ~equal:Char.( = ))
    && List.mem bottom_pipes pipe ~equal:Char.( = )
;;

let find_available_pipes sketch (y, x) =
  [ Top, -1, 0; Bottom, 1, 0; Left, 0, -1; Right, 0, 1 ]
  |> List.map ~f:(fun (side, dy, dx) ->
    if y + dy < 0
       || y + dy > Array.length sketch - 1
       || x + dx < 0
       || x + dx > Array.length sketch.(0) - 1
    then None
    else if is_valid_pipe sketch.(y + dy).(x + dx) side sketch.(y).(x)
    then Some (sketch.(y + dy).(x + dx), (y + dy, x + dx))
    else None)
  |> List.filter_opt
;;

let rec add_to_graph (sketch : char array array) graph (queue : (int * int) list) =
  match queue with
  | [] -> graph
  | (y, x) :: _ when Char.( = ) sketch.(y).(x) 'S' && Map.mem graph (y, x) -> graph
  | (y, x) :: tail when Map.mem graph (y, x) -> add_to_graph sketch graph tail
  | (y, x) :: tail ->
    let found_pipes =
      find_available_pipes sketch (y, x)
      |> List.filter ~f:(fun (_, pos) -> not (Map.mem graph pos))
    in
    let updated_graph =
      found_pipes
      |> List.fold ~init:graph ~f:(fun acc pipe ->
        Map.update acc (y, x) ~f:(fun pipes ->
          match pipes with
          | Some pipes -> pipe :: pipes
          | None -> [ pipe ]))
    in
    add_to_graph sketch updated_graph (tail @ (found_pipes |> List.map ~f:snd))
;;

let create_graph (input : string list) =
  let sketch = input |> Array.of_list |> Array.map ~f:String.to_array in
  let flat_input = input |> String.concat in
  let start_position =
    match flat_input |> String.findi ~f:(fun _ c -> Char.( = ) c 'S') with
    | None -> failwith "no start point in input"
    | Some (index, _) -> point_from_index index (Array.length sketch.(0))
  in
  let graph = add_to_graph sketch PipesMap.empty [ start_position ] in
  graph, start_position
;;

let () =
  let input = In_channel.read_lines "days/day10/input.txt" in
  let graph, _ = create_graph input in
  let result = (Map.length graph + 1) / 2 in
  printf "PART1: %d\n" result
;;
