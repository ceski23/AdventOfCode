open Core

type range =
  { start : int
  ; length : int
  ; mapped_value : int
  }

type 'a tree =
  | Node of 'a * 'a tree * 'a tree
  | Leaf

let rec find_matching_range (searched_value : int) (tree : range tree) =
  match tree with
  | Leaf -> None
  | Node (node_value, left_sub_tree, right_sub_tree) ->
    if searched_value < node_value.start
    then find_matching_range searched_value left_sub_tree
    else if searched_value > node_value.start
    then
      if searched_value < node_value.start + node_value.length
      then Some node_value
      else find_matching_range searched_value right_sub_tree
    else Some node_value
;;

let rec add_range_to_tree (item : range) (tree : range tree) =
  match tree with
  | Leaf -> Node (item, Leaf, Leaf)
  | Node (node_value, left_sub_tree, right_sub_tree) as t ->
    if item.start < node_value.start
    then Node (node_value, add_range_to_tree item left_sub_tree, right_sub_tree)
    else if item.start > node_value.start
    then Node (node_value, left_sub_tree, add_range_to_tree item right_sub_tree)
    else t
;;

let parse_seeds line =
  line
  |> Re2.get_matches_exn (Re2.create_exn "\\d+")
  |> List.map ~f:(fun m -> Re2.Match.get_exn m ~sub:(`Index 0) |> Int.of_string)
;;

let parse_map_section (section : string) =
  List.drop (section |> String.split_lines) 1
  |> List.fold ~init:Leaf ~f:(fun acc x ->
    let numbers = String.split x ~on:' ' |> List.map ~f:int_of_string |> Array.of_list in
    add_range_to_tree
      { start = numbers.(1); mapped_value = numbers.(0); length = numbers.(2) }
      acc)
;;

let find_seed_location (mappings : range tree list) seed =
  List.fold mappings ~init:seed ~f:(fun acc mapping ->
    match find_matching_range acc mapping with
    | Some v -> v.mapped_value + (acc - v.start)
    | None -> acc)
;;

let parse_input input =
  let sections = input |> Re2.split (Re2.create_exn "\\n\\n") in
  let mappings = List.drop sections 1 |> List.map ~f:parse_map_section in
  let seeds =
    List.nth_exn sections 0
    |> Re2.get_matches_exn (Re2.create_exn "\\d+")
    |> List.map ~f:(fun m -> Re2.Match.get_exn m ~sub:(`Index 0) |> Int.of_string)
  in
  mappings, seeds
;;

let () =
  let result =
    let mappings, seeds = parse_input (In_channel.read_all "days/day5/input.txt") in
    seeds
    |> List.map ~f:(find_seed_location mappings)
    |> List.min_elt ~compare:compare_int
    |> Option.value_exn
  in
  printf "PART1: %d\n" result;
  assert (result = 389056265)
;;

let () =
  let mappings, seeds = parse_input (In_channel.read_all "days/day5/input.txt") in
  let result =
    seeds
    |> List.chunks_of ~length:2
    |> List.fold ~init:Int.max_value ~f:(fun acc range ->
      let start = List.nth_exn range 0 in
      let length = List.nth_exn range 1 in
      let seeds = Seq.init length (fun i -> i + start) in
      let min_in_range =
        Seq.fold_left
          (fun acc seed -> min acc (find_seed_location mappings seed))
          Int.max_value
          seeds
      in
      min acc min_in_range)
  in
  printf "PART2: %d\n" result;
  assert (result = 137516820)
;;
