open Core

let number_regex = Re2.create_exn "(\\d+)"

let is_part_number (matrix : char array array) (m : Re2.Match.t) =
  let matrix_width, matrix_height =
    Array.last matrix |> Array.length, Array.length matrix
  in
  let start, length = Re2.Match.get_pos_exn ~sub:(`Index 0) m in
  let x, y =
    ( start mod matrix_width
    , Float.round_down (float start /. float matrix_height) |> int_of_float )
  in
  let pairs =
    List.cartesian_product
      [ -1; 0; 1 ]
      (List.init (length + 2) ~f:(fun index -> -1 + index))
    |> List.filter ~f:(fun (dy, dx) ->
      (not (x + dx <> -1 && x + dx <> start + length && y + dy = 0))
      && y + dy >= 0
      && y + dy < matrix_height
      && x + dx >= 0
      && x + dx < matrix_width)
  in
  let _is_not =
    List.for_all pairs ~f:(fun (dy, dx) ->
      Char.equal matrix.(y + dy).(x + dx) '.' || Char.is_digit matrix.(y + dy).(x + dx))
  in
  not _is_not
;;

let sum_part_numbers input =
  let input_line = String.concat input in
  let input_matrix = input |> List.to_array |> Array.map ~f:String.to_array in
  let number_matches = Re2.get_matches_exn number_regex input_line in
  List.fold
    ~init:0
    ~f:(fun acc m ->
      let n = Re2.Match.get_exn ~sub:(`Index 0) m |> Int.of_string in
      match is_part_number input_matrix m with
      | true -> acc + n
      | false -> acc)
    number_matches
;;

let () =
  let result = In_channel.read_lines "days/day3/input.txt" |> sum_part_numbers in
  printf "PART1: %d\n" result;
  assert (result = 526404)
;;
