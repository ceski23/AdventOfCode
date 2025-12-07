use itertools::Itertools;
use std::{ops::RangeInclusive, str::Lines};

fn fresh_ids(lines: &mut Lines) -> Vec<RangeInclusive<u64>> {
    lines
        .take_while_ref(|x| !x.is_empty())
        .filter_map(|x| {
            let (start, end) = x.split_once("-")?;
            let start_num = start.parse::<u64>().ok()?;
            let end_num = end.parse::<u64>().ok()?;

            Some(start_num..=end_num)
        })
        .collect_vec()
}

fn available_fresh_count(text: String) -> usize {
    let mut lines = text.lines();
    let fresh_ids = fresh_ids(&mut lines);

    lines
        .filter_map(|line| line.parse::<u64>().ok())
        .filter(|id| fresh_ids.iter().any(|range| range.contains(id)))
        .count()
}

fn all_fresh_count(text: String) -> u64 {
    let fresh_ids = fresh_ids(&mut text.lines())
        .into_iter()
        .sorted_by_key(|range| *range.start())
        .collect_vec();

    let mut count = 0;
    let mut max_end = u64::MIN;

    for range in fresh_ids {
        if *range.start() > max_end + 1 {
            count += *range.end() - *range.start() + 1;
        } else if *range.end() > max_end {
            count += *range.end() - max_end;
        }

        max_end = max_end.max(*range.end());
    }

    count
}

#[cfg(test)]
mod tests {
    use super::*;
    use anyhow::Result;
    use std::fs;

    #[test]
    fn part1_test() -> Result<()> {
        let input = fs::read_to_string("inputs/day05_test.txt")?;
        assert_eq!(available_fresh_count(input), 3);

        Ok(())
    }

    #[test]
    fn part1() -> Result<()> {
        let input = fs::read_to_string("inputs/day05.txt")?;
        assert_eq!(available_fresh_count(input), 735);

        Ok(())
    }

    #[test]
    fn part2_test() -> Result<()> {
        let input = fs::read_to_string("inputs/day05_test.txt")?;
        assert_eq!(all_fresh_count(input), 14);

        Ok(())
    }

    #[test]
    fn part2() -> Result<()> {
        let input = fs::read_to_string("inputs/day05.txt")?;
        assert_eq!(all_fresh_count(input), 344306344403172);

        Ok(())
    }
}
