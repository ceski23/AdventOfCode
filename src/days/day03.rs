use anyhow::Result;
use itertools::Itertools;

fn parse_input(text: String) -> Result<Vec<Vec<u64>>> {
    let batteries_banks = text
        .lines()
        .map(|line| {
            line.chars()
                .filter_map(|char| char.to_digit(10).map(u64::from))
                .collect_vec()
        })
        .collect_vec();

    Ok(batteries_banks)
}

fn find_biggest_joltage(batteries: &[u64], count: usize) -> Result<u64> {
    let mut digits_indices = (1..=count)
        .rev()
        .map(|value| batteries.len() - value)
        .collect_vec();

    for (index, digit) in digits_indices.clone().iter().enumerate() {
        let iterator_start = index.checked_sub(1).map_or(0, |i| digits_indices[i] + 1);

        for new_digit in (iterator_start..*digit).rev() {
            if batteries[new_digit] >= batteries[digits_indices[index]] {
                digits_indices[index] = new_digit
            }
        }
    }

    let number = digits_indices
        .iter()
        .rev()
        .enumerate()
        .fold(0, |acc, (index, digit_index)| {
            acc + (10u64.pow(index as _) * batteries[*digit_index])
        });

    Ok(number)
}

fn sum_joltages(banks: Vec<Vec<u64>>, count: usize) -> Result<u64> {
    banks
        .iter()
        .map(|batteries| find_biggest_joltage(batteries, count))
        .sum()
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs;

    #[test]
    fn part1_test() -> Result<()> {
        let input = fs::read_to_string("inputs/day03_test.txt")?;
        let data = parse_input(input)?;
        assert_eq!(sum_joltages(data, 2)?, 357);

        Ok(())
    }

    #[test]
    fn part1() -> Result<()> {
        let input = fs::read_to_string("inputs/day03.txt")?;
        let data = parse_input(input)?;
        assert_eq!(sum_joltages(data, 2)?, 17435);

        Ok(())
    }

    #[test]
    fn part2_test() -> Result<()> {
        let input = fs::read_to_string("inputs/day03_test.txt")?;
        let data = parse_input(input)?;
        assert_eq!(sum_joltages(data, 12)?, 3121910778619);

        Ok(())
    }

    #[test]
    fn part2() -> Result<()> {
        let input = fs::read_to_string("inputs/day03.txt")?;
        let data = parse_input(input)?;
        assert_eq!(sum_joltages(data, 12)?, 172886048065379);

        Ok(())
    }
}
