open Core
module NumbersSet = Set.Make (Int)
module ScratchcardsMap = Map.Make (Int)

let parse_numbers line =
  line
  |> Re2.split (Re2.create_exn "\\s+")
  |> List.filter ~f:(fun x -> not (String.is_empty x))
  |> List.map ~f:Int.of_string
  |> NumbersSet.of_list
;;

let parse_scratchcard line =
  let matches =
    Re2.first_match_exn
      (Re2.create_exn
         "Card\\s+(?P<card_id>\\d+): (?P<winning_numbers>.*?) \\| (?P<my_numbers>.*)$")
      line
  in
  let card_id = Re2.Match.get_exn matches ~sub:(`Name "card_id") |> Int.of_string in
  let winning_numbers =
    parse_numbers (Re2.Match.get_exn matches ~sub:(`Name "winning_numbers"))
  in
  let my_numbers = parse_numbers (Re2.Match.get_exn matches ~sub:(`Name "my_numbers")) in
  let matched_numbers = Set.inter my_numbers winning_numbers |> Set.to_list in
  card_id, matched_numbers
;;

let calc_points line =
  let _, matched_numbers = parse_scratchcard line in
  List.foldi
    ~init:0
    ~f:(fun index acc _ ->
      acc + if index = 0 then 1 else 2. ** float (index - 1) |> int_of_float)
    matched_numbers
;;

let () =
  let result =
    In_channel.with_file
      "days/day4/input.txt"
      ~f:(In_channel.fold_lines ~init:0 ~f:(fun acc x -> acc + calc_points x))
  in
  printf "PART1: %d\n" result;
  assert (result = 21568)
;;

let get_new_cards (card_id : int) (cards : int list ScratchcardsMap.t) =
  let numbers = Map.find_exn cards card_id in
  let new_card_ids =
    List.init (List.length numbers) ~f:(fun index -> card_id + index + 1)
  in
  new_card_ids
;;

let resolve_won_scratchcard (cards : int list ScratchcardsMap.t) =
  let rec _resolve_won_scratchcard
    (queue : int list)
    (final : int list)
    (cards : int list ScratchcardsMap.t)
    =
    match queue with
    | [] -> final
    | [ head ] ->
      _resolve_won_scratchcard (get_new_cards head cards) (head :: final) cards
    | head :: tail ->
      _resolve_won_scratchcard
        (List.append (get_new_cards head cards) tail)
        (head :: final)
        cards
  in
  _resolve_won_scratchcard (Map.keys cards) [] cards
;;

let count_won_scratchcards (lines : string list) =
  let cards =
    List.fold
      ~init:ScratchcardsMap.empty
      ~f:(fun acc line ->
        let card_id, matched_numbers = parse_scratchcard line in
        Map.set acc ~key:card_id ~data:matched_numbers)
      lines
  in
  resolve_won_scratchcard cards |> List.length
;;

let () =
  let result = In_channel.read_lines "days/day4/input.txt" |> count_won_scratchcards in
  printf "PART2: %d\n" result;
  assert (result = 11827296)
;;
