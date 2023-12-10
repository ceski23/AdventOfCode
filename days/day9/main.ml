let parse_line line =
  line |> Core.String.split ~on:' ' |> Array.of_list |> Array.map int_of_string
;;

let sliding_window array =
  Seq.map2 (fun a b -> a, b) (array |> Array.to_seq) (array |> Array.to_seq |> Seq.drop 1)
  |> Array.of_seq
;;

let calculate_next_lines (first_line : int array) =
  let rec _calculate_next_lines lines =
    if Array.for_all (fun x -> x = 0) lines.(0)
    then lines |> Core.Array.rev
    else (
      let next_line = lines.(0) |> sliding_window |> Array.map (fun (a, b) -> b - a) in
      _calculate_next_lines (Array.append [| next_line |] lines))
  in
  _calculate_next_lines [| first_line |]
;;

let extrapolate_right lines =
  lines |> Core.Array.fold ~init:0 ~f:(fun acc line -> acc + Core.Array.last line)
;;

let () =
  Core.In_channel.with_file "days/day9/input.txt" ~f:(fun file ->
    let result =
      Core.In_channel.fold_lines file ~init:0 ~f:(fun acc line ->
        line |> parse_line |> calculate_next_lines |> extrapolate_right |> ( + ) acc)
    in
    Core.printf "PART1: %d\n" result;
    assert (result = 1934898178))
;;

let extrapolate_left lines =
  lines
  |> Core.Array.foldi ~init:0 ~f:(fun index acc line ->
    acc + (line.(0) * Int.of_float (-1.0 ** float index)))
;;

let () =
  Core.In_channel.with_file "days/day9/input.txt" ~f:(fun file ->
    let result =
      Core.In_channel.fold_lines file ~init:0 ~f:(fun acc line ->
        line |> parse_line |> calculate_next_lines |> extrapolate_left |> ( + ) acc)
    in
    Core.printf "PART2: %d\n" result;
    assert (result = 1129))
;;
