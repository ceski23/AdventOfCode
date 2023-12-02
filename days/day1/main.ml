open Core

let digits_regex = Re2.create_exn "[1-9]"

let digits_with_words_regex =
  Re2.create_exn
    "[1-9]|oneight|twone|threeight|fiveight|sevenine|eightwo|eighthree|nineight|one|two|three|four|five|six|seven|eight|nine"
;;

let digit_string_to_digits number =
  match number with
  | "one" -> [ 1 ]
  | "two" -> [ 2 ]
  | "three" -> [ 3 ]
  | "four" -> [ 4 ]
  | "five" -> [ 5 ]
  | "six" -> [ 6 ]
  | "seven" -> [ 7 ]
  | "eight" -> [ 8 ]
  | "nine" -> [ 9 ]
  | x -> [ Int.of_string x ]
;;

let number_string_to_digits number =
  match number with
  | "oneight" -> [ 1; 8 ]
  | "twone" -> [ 2; 1 ]
  | "threeight" -> [ 3; 8 ]
  | "fiveight" -> [ 5; 8 ]
  | "sevenine" -> [ 7; 9 ]
  | "eightwo" -> [ 8; 2 ]
  | "eighthree" -> [ 8; 3 ]
  | "nineight" -> [ 9; 8 ]
  | x -> digit_string_to_digits x
;;

let rec first_and_last list =
  match list with
  | [] -> failwith "bad data"
  | [ first ] -> first, first
  | [ first; second ] -> first, second
  | first :: _ :: tail -> first_and_last (first :: tail)
;;

let flatten list_of_lists =
  let rec _flatten acc = function
    | [] -> List.rev acc
    | list :: tail -> _flatten (List.rev_append list acc) tail
  in
  _flatten [] list_of_lists
;;

let parse_line line =
  let digits =
    match Re2.find_all digits_regex line with
    | Ok matches -> List.map ~f:digit_string_to_digits matches |> flatten
    | Error _ -> []
  in
  first_and_last digits |> fun (a, b) -> (a * 10) + b
;;

let parse_line_with_words line =
  let digits =
    match Re2.find_all digits_with_words_regex line with
    | Ok matches -> List.map ~f:number_string_to_digits matches |> flatten
    | Error _ -> []
  in
  first_and_last digits |> fun (a, b) -> (a * 10) + b
;;

let () =
  In_channel.with_file
    "days/day1/input.txt"
    ~f:(In_channel.fold_lines ~init:0 ~f:(fun acc number -> acc + parse_line number))
  |> printf "PART1: %d\n"
;;

let () =
  In_channel.with_file
    "days/day1/input.txt"
    ~f:
      (In_channel.fold_lines ~init:0 ~f:(fun acc number ->
         acc + parse_line_with_words number))
  |> printf "PART2: %d\n"
;;
