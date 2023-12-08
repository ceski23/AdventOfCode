open Core

type hand =
  | FiveOfAKind of char list
  | FourOFAKind of char list
  | FullHouse of char list
  | ThreeOfAKind of char list
  | TwoPair of char list
  | OnePair of char list
  | HighCard of char list

let find_most_common_card (cards : char list) =
  cards
  |> List.sort_and_group ~compare:compare_char
  |> List.fold ~init:('X', 0) ~f:(fun (char, count) cards_group ->
    let len = List.length cards_group in
    let new_char = List.last_exn cards_group in
    if count < len && Char.( <> ) new_char 'J' then new_char, len else char, count)
  |> fst
;;

let parse_hand (replace_joker : bool) (hand : char list) =
  let cards_to_group =
    if replace_joker
    then (
      let replacement = hand |> find_most_common_card in
      hand |> List.map ~f:(fun card -> if Char.equal card 'J' then replacement else card))
    else hand
  in
  let groups = List.sort_and_group ~compare:compare_char cards_to_group in
  if List.length groups = 1
  then FiveOfAKind hand
  else if List.length groups = 2
          && List.for_all groups ~f:(fun x -> List.length x = 4 || List.length x = 1)
  then FourOFAKind hand
  else if List.length groups = 2
          && List.for_all groups ~f:(fun x -> List.length x = 3 || List.length x = 2)
  then FullHouse hand
  else if List.length groups = 3
          && List.for_all groups ~f:(fun x -> List.length x = 3 || List.length x = 1)
  then ThreeOfAKind hand
  else if List.length groups = 3
          && List.for_all groups ~f:(fun x -> List.length x = 2 || List.length x = 1)
  then TwoPair hand
  else if List.length groups = 4
  then OnePair hand
  else HighCard hand
;;

let parse_input (replace_joker : bool) (input : string list) =
  input
  |> List.map ~f:(fun line ->
    String.split_on_chars ~on:[ ' ' ] line
    |> function
    | [ hand; bid ] -> String.to_list hand |> parse_hand replace_joker, Int.of_string bid
    | _ -> failwith "invalid data")
;;

let rec compare_same_types (cards_order : char list) (a : char list) (b : char list) =
  match a, b with
  | head_a :: tail_a, head_b :: tail_b ->
    if Char.equal head_a head_b
    then compare_same_types cards_order tail_a tail_b
    else (
      let index_a, _ = List.findi_exn cards_order ~f:(fun _ x -> Char.equal x head_a) in
      let index_b, _ = List.findi_exn cards_order ~f:(fun _ x -> Char.equal x head_b) in
      Int.compare index_b index_a)
  | _, _ -> failwith "bad input"
;;

let compare_hands_with_bid (cards_order : char list) (a : hand * int) (b : hand * int) =
  match a |> fst, b |> fst with
  | ( FiveOfAKind _
    , (FourOFAKind _ | FullHouse _ | ThreeOfAKind _ | TwoPair _ | OnePair _ | HighCard _)
    )
  | FourOFAKind _, (FullHouse _ | ThreeOfAKind _ | TwoPair _ | OnePair _ | HighCard _)
  | FullHouse _, (ThreeOfAKind _ | TwoPair _ | OnePair _ | HighCard _)
  | ThreeOfAKind _, (TwoPair _ | OnePair _ | HighCard _)
  | TwoPair _, (OnePair _ | HighCard _)
  | OnePair _, HighCard _ -> -1
  | FiveOfAKind a, FiveOfAKind b
  | FourOFAKind a, FourOFAKind b
  | FullHouse a, FullHouse b
  | ThreeOfAKind a, ThreeOfAKind b
  | TwoPair a, TwoPair b
  | OnePair a, OnePair b
  | HighCard a, HighCard b -> compare_same_types cards_order a b
  | _ -> 1
;;

let calc_total_winnings hands =
  List.foldi hands ~init:0 ~f:(fun index acc (_, bid) ->
    acc + (bid * (List.length hands - index)))
;;

let () =
  let cards_order = [ '2'; '3'; '4'; '5'; '6'; '7'; '8'; '9'; 'T'; 'J'; 'Q'; 'K'; 'A' ] in
  let result =
    In_channel.read_lines "days/day7/input.txt"
    |> parse_input false
    |> List.sort ~compare:(compare_hands_with_bid cards_order)
    |> calc_total_winnings
  in
  printf "PART1: %d\n" result;
  assert (result = 250370104)
;;

let () =
  let cards_order = [ 'J'; '2'; '3'; '4'; '5'; '6'; '7'; '8'; '9'; 'T'; 'Q'; 'K'; 'A' ] in
  let result =
    In_channel.read_lines "days/day7/input.txt"
    |> parse_input true
    |> List.sort ~compare:(compare_hands_with_bid cards_order)
    |> calc_total_winnings
  in
  printf "PART2: %d\n" result;
  assert (result = 251735672)
;;
