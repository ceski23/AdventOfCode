open Core
module NetworkMap = Map.Make (String)

let rec gcd a b = if b = 0 then a else gcd b (a mod b)
let lcm a b = a / gcd a b * b

let parse_network_node line =
  let first_match =
    Re2.first_match_exn
      (Re2.create_exn
         "(?P<node_from>\\w{3}) = \\((?P<node_left>\\w{3}), (?P<node_right>\\w{3})\\)")
      line
  in
  let node_from = Re2.Match.get_exn first_match ~sub:(`Name "node_from") in
  let node_left = Re2.Match.get_exn first_match ~sub:(`Name "node_left") in
  let node_right = Re2.Match.get_exn first_match ~sub:(`Name "node_right") in
  node_from, node_left, node_right
;;

let parse_input (input : string) =
  let sections = input |> Re2.split (Re2.create_exn "\\n\\n") in
  let directions = List.nth_exn sections 0 |> String.to_array in
  let network =
    List.nth_exn sections 1
    |> String.split_lines
    |> List.fold ~init:NetworkMap.empty ~f:(fun acc line ->
      let node_from, node_left, node_right = parse_network_node line in
      Map.set acc ~key:node_from ~data:(node_left, node_right))
  in
  directions, network
;;

let rec traverse_network
  (directions : char array)
  (network : (string * string) NetworkMap.t)
  ?(steps : int = 0)
  ?(index : int = 0)
  (should_stop : string -> bool)
  (start_node : string)
  =
  if should_stop start_node
  then steps
  else (
    let next_node =
      match directions.(index) with
      | 'L' -> Map.find_exn network start_node |> fst
      | 'R' -> Map.find_exn network start_node |> snd
      | _ -> failwith "invalid data"
    in
    let next_index = (index + 1) mod Array.length directions in
    traverse_network
      directions
      network
      ?steps:(Some (steps + 1))
      ?index:(Some next_index)
      should_stop
      next_node)
;;

let () =
  let directions, network = parse_input (In_channel.read_all "days/day8/input.txt") in
  let result = traverse_network directions network (String.equal "ZZZ") "AAA" in
  printf "PART1: %d\n" result;
  assert (result = 20513)
;;

let () =
  let directions, network = parse_input (In_channel.read_all "days/day8/input.txt") in
  let result =
    Map.keys network
    |> List.filter ~f:(fun node -> String.is_suffix node ~suffix:"A")
    |> List.map ~f:(traverse_network directions network (String.is_suffix ~suffix:"Z"))
    |> List.fold ~init:1 ~f:(fun acc length -> lcm acc length)
  in
  printf "PART2: %d\n" result;
  assert (result = 15995167053923)
;;
