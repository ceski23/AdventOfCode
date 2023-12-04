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

module GearsMap = Map.Make (IntPairs)

let get_adjacent_symbols (matrix : char array array) (m : Re2.Match.t) =
  let matrix_width, matrix_height =
    Array.last matrix |> Array.length, Array.length matrix
  in
  let start, length = Re2.Match.get_pos_exn ~sub:(`Index 0) m in
  let x, y =
    ( start mod matrix_width
    , Float.round_down (float start /. float matrix_height) |> int_of_float )
  in
  let points =
    List.cartesian_product
      [ -1; 0; 1 ]
      (List.init (length + 2) ~f:(fun index -> -1 + index))
    |> List.map ~f:(fun (dy, dx) -> y + dy, x + dx)
    |> List.filter ~f:(fun (y, x) ->
      y >= 0 && y < matrix_height && x >= 0 && x < matrix_width)
  in
  List.fold points ~init:[] ~f:(fun acc (y, x) ->
    match matrix.(y).(x) with
    | c when Char.equal c '.' || Char.is_digit c -> acc
    | c -> (c, (y, x)) :: acc)
;;

let is_part_number (matrix : char array array) (m : Re2.Match.t) =
  get_adjacent_symbols matrix m |> List.length > 0
;;

let parse_input input =
  let input_line = String.concat input in
  let input_matrix = input |> List.to_array |> Array.map ~f:String.to_array in
  let number_matches = Re2.get_matches_exn (Re2.create_exn "(\\d+)") input_line in
  input_matrix, number_matches
;;

let sum_part_numbers input =
  let input_matrix, number_matches = parse_input input in
  List.fold number_matches ~init:0 ~f:(fun acc m ->
    let n = Re2.Match.get_exn ~sub:(`Index 0) m |> Int.of_string in
    if is_part_number input_matrix m then acc + n else acc)
;;

let () =
  let result = In_channel.read_lines "days/day3/input.txt" |> sum_part_numbers in
  printf "PART1: %d\n" result;
  assert (result = 526404)
;;

let sum_gear_ratios input =
  let input_matrix, number_matches = parse_input input in
  let gear_symbols =
    List.fold number_matches ~init:GearsMap.empty ~f:(fun acc m ->
      let n = Re2.Match.get_exn ~sub:(`Index 0) m |> Int.of_string in
      let symbols = get_adjacent_symbols input_matrix m in
      List.fold symbols ~init:acc ~f:(fun acc (symbol, point) ->
        match symbol with
        | '*' ->
          Map.update acc point ~f:(fun numbers ->
            match numbers with
            | Some numbers -> n :: numbers
            | None -> [ n ])
        | _ -> acc))
  in
  Map.data gear_symbols
  |> List.fold ~init:0 ~f:(fun acc numbers ->
    match numbers with
    | [ a; b ] -> acc + (a * b)
    | _ -> acc)
;;

let () =
  let result = In_channel.read_lines "days/day3/input.txt" |> sum_gear_ratios in
  printf "PART2: %d\n" result;
  assert (result = 84399773)
;;
