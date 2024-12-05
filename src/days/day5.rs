use anyhow::{Ok, Result};
use itertools::Itertools;
use std::collections::HashMap;

type Pairs = Vec<(u32, u32)>;
type UpdatesList = Vec<Vec<u32>>;

fn parse_pairs(text: &str) -> Pairs {
    text.lines()
        .filter_map(|line| {
            let (a, b) = line.split_once("|")?;
            let a_num = a.parse::<u32>().ok()?;
            let b_num = b.parse::<u32>().ok()?;

            Some((a_num, b_num))
        })
        .collect()
}

fn parse_updates_list(text: &str) -> UpdatesList {
    text.lines()
        .map(|line| {
            line.split(",")
                .filter_map(|item| item.parse::<u32>().ok())
                .collect()
        })
        .collect()
}

fn parse_input(input: String) -> Result<(Pairs, UpdatesList)> {
    let (pairs, updates_list) = input
        .split_once("\n\n")
        .ok_or(anyhow::anyhow!("Invalid input"))?;

    Ok((parse_pairs(pairs), parse_updates_list(updates_list)))
}

fn get_middle_page(update: &[u32]) -> u32 {
    update[update.len().div_floor(2)]
}

fn sum_correctly_ordered_updates(pairs: Pairs, updates_list: UpdatesList) -> u32 {
    pairs
        .iter()
        .fold(updates_list, |valid_updates, (a, b)| {
            valid_updates
                .iter()
                .filter(|update| {
                    let a_index = update.iter().position(|page| page == a);
                    let b_index = update.iter().position(|page| page == b);

                    match (a_index, b_index) {
                        (Some(a_index), Some(b_index)) => a_index < b_index,
                        _ => true,
                    }
                })
                .cloned()
                .collect()
        })
        .iter()
        .map(|update| get_middle_page(update))
        .sum()
}

fn sum_fixed_updates(pairs: Pairs, updates_list: UpdatesList) -> u32 {
    updates_list
        .iter()
        .filter_map(|updates| {
            let mut counts_map = HashMap::<&u32, u32>::new();

            pairs.iter().for_each(|(a, b)| {
                if updates.contains(a) && updates.contains(b) {
                    counts_map
                        .entry(a)
                        .and_modify(|count| *count += 1)
                        .or_insert(1);
                    counts_map.entry(b).or_default();
                }
            });

            let ordered = counts_map
                .iter()
                .sorted_by_key(|(_, count)| **count)
                .map(|(page, _)| **page)
                .rev()
                .collect::<Vec<u32>>();

            if ordered == *updates {
                None
            } else {
                Some(ordered)
            }
        })
        .map(|update| get_middle_page(&update))
        .sum()
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs;

    #[test]
    fn part1_test() -> Result<()> {
        let input = fs::read_to_string("inputs/day5_test.txt")?;
        let (pairs, updates) = parse_input(input)?;
        assert_eq!(sum_correctly_ordered_updates(pairs, updates), 143);

        Ok(())
    }

    #[test]
    fn part1() -> Result<()> {
        let input = fs::read_to_string("inputs/day5.txt")?;
        let (pairs, updates) = parse_input(input)?;
        assert_eq!(sum_correctly_ordered_updates(pairs, updates), 4135);

        Ok(())
    }

    #[test]
    fn part2_test() -> Result<()> {
        let input = fs::read_to_string("inputs/day5_test.txt")?;
        let (pairs, updates) = parse_input(input)?;
        assert_eq!(sum_fixed_updates(pairs, updates), 123);

        Ok(())
    }

    #[test]
    fn part2() -> Result<()> {
        let input = fs::read_to_string("inputs/day5.txt")?;
        let (pairs, updates) = parse_input(input)?;
        assert_eq!(sum_fixed_updates(pairs, updates), 5285);

        Ok(())
    }
}
