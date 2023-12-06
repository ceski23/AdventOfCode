open Core

let parse_int_line line =
  line
  |> Re2.get_matches_exn (Re2.create_exn "\\d+")
  |> List.map ~f:(fun m -> Re2.Match.get_exn m ~sub:(`Index 0) |> Int.of_string)
;;

let calc_distance button_time total_time = button_time * (total_time - button_time)

let _find_win_count times distances =
  List.fold2_exn times distances ~init:1 ~f:(fun acc time distance ->
    let win_count =
      Seq.init time (fun index -> calc_distance (index + 1) time)
      |> Seq.filter (fun d -> d > distance)
      |> Seq.length
    in
    acc * win_count)
;;

let find_win_count2 times distances =
  List.fold2_exn times distances ~init:1 ~f:(fun acc time distance ->
    let win_count =
      let x1 =
        0.5 *. (float time -. sqrt ((float time ** 2.0) -. float (4 * distance)))
        |> Float.iround_down_exn
      in
      let x2 =
        0.5 *. (sqrt ((float time ** 2.0) -. float (4 * distance)) +. float time)
        |> Float.iround_up_exn
      in
      x2 - x1 - 1
    in
    acc * win_count)
;;

let () =
  let result =
    let input = In_channel.read_lines "days/day6/input.txt" in
    let times = parse_int_line (List.nth_exn input 0) in
    let distances = parse_int_line (List.nth_exn input 1) in
    find_win_count2 times distances
  in
  printf "PART1: %d\n" result;
  assert (result = 5133600)
;;

let fix_kerning (numbers : int list) =
  numbers |> List.map ~f:string_of_int |> String.concat |> Int.of_string
;;

let () =
  let result =
    let input = In_channel.read_lines "days/day6/input.txt" in
    let time = parse_int_line (List.nth_exn input 0) |> fix_kerning in
    let distance = parse_int_line (List.nth_exn input 1) |> fix_kerning in
    find_win_count2 [ time ] [ distance ]
  in
  printf "PART2: %d\n" result;
  assert (result = 40651271)
;;
