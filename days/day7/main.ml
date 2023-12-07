open Core
module CardsSet = Set.Make (Char)

type hand =
  | FiveOfAKind of char list
  | FourOFAKind of char list
  | FullHouse of char list
  | ThreeOfAKind of char list
  | TwoPair of char list
  | OnePair of char list
  | HighCard of char list

let find_most_common_card (cards : char list) =
  let card, _ =
    cards
    |> List.sort_and_group ~compare:compare_char
    |> List.fold ~init:('X', 0) ~f:(fun (char, count) cards_group ->
      let len = List.length cards_group in
      let new_char = List.last_exn cards_group in
      if count < len && Char.( <> ) new_char 'J' then new_char, len else char, count)
  in
  card
;;

let parse_hand (replace_joker : bool) (hand : char list) =
  let cards_to_group =
    if replace_joker
    then
      hand
      |> String.of_list
      |> String.substr_replace_all
           ~pattern:"J"
           ~with_:(hand |> find_most_common_card |> String.of_char)
      |> String.to_list
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

let compare_cards (a : char) (b : char) =
  let cards_order =
    [ 'A'; 'K'; 'Q'; 'J'; 'T'; '9'; '8'; '7'; '6'; '5'; '4'; '3'; '2' ] |> List.rev
  in
  let a_index, _ = List.findi_exn cards_order ~f:(fun _ x -> Char.equal x a) in
  let b_index, _ = List.findi_exn cards_order ~f:(fun _ x -> Char.equal x b) in
  Int.compare a_index b_index
;;

let rec compare_same_hands (a : char list) (b : char list) =
  match a, b with
  | ha :: ta, hb :: tb ->
    if Char.equal ha hb then compare_same_hands ta tb else compare_cards ha hb
  | _, _ -> failwith "bad input"
;;

let compare_hands_with_bid (a : hand * int) (b : hand * int) =
  let hand_a, _ = a in
  let hand_b, _ = b in
  match hand_a, hand_b with
  | ( FiveOfAKind _
    , (FourOFAKind _ | FullHouse _ | ThreeOfAKind _ | TwoPair _ | OnePair _ | HighCard _)
    )
  | FourOFAKind _, (FullHouse _ | ThreeOfAKind _ | TwoPair _ | OnePair _ | HighCard _)
  | FullHouse _, (ThreeOfAKind _ | TwoPair _ | OnePair _ | HighCard _)
  | ThreeOfAKind _, (TwoPair _ | OnePair _ | HighCard _)
  | TwoPair _, (OnePair _ | HighCard _)
  | OnePair _, HighCard _ -> 1
  | FiveOfAKind a, FiveOfAKind b
  | FourOFAKind a, FourOFAKind b
  | FullHouse a, FullHouse b
  | ThreeOfAKind a, ThreeOfAKind b
  | TwoPair a, TwoPair b
  | OnePair a, OnePair b
  | HighCard a, HighCard b -> compare_same_hands a b
  | _ -> -1
;;

let () =
  let hands =
    parse_input false (In_channel.read_lines "days/day7/test.txt")
    |> List.sort ~compare:compare_hands_with_bid
    |> List.rev
  in
  let result =
    List.foldi hands ~init:0 ~f:(fun index acc (_, bid) ->
      let rank = List.length hands - index in
      (* (match hand with
         | FiveOfAKind _ -> printf "FiveOFAKind %d * %d\n" bid rank
         | FourOFAKind _ -> printf "FourOFAKind %d * %d\n" bid rank
         | FullHouse _ -> printf "FullHouse %d * %d\n" bid rank
         | ThreeOfAKind _ -> printf "ThreeOfAKind %d * %d\n" bid rank
         | TwoPair _ -> printf "TwoPair %d * %d\n" bid rank
         | OnePair _ -> printf "OnePair %d * %d\n" bid rank
         | HighCard _ -> printf "HighCard %d * %d\n" bid rank); *)
      acc + (bid * rank))
  in
  printf "PART1: %d\n" result
;;

(* assert (result = 250370104) *)

let () =
  let hands =
    parse_input true (In_channel.read_lines "days/day7/test.txt")
    |> List.sort ~compare:compare_hands_with_bid
    |> List.rev
  in
  let result =
    List.foldi hands ~init:0 ~f:(fun index acc (_, bid) ->
      acc + ((bid * List.length hands) - index))
  in
  printf "PART2: %d\n" result
;;
