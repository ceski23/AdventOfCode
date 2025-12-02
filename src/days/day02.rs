use anyhow::Result;
use rayon::prelude::*;
use regress::Regex;

fn parse_input(text: String) -> Result<Vec<u64>> {
    let numbers = Regex::new(r"((\d+)-(\d+))")?
        .find_iter(&text)
        .filter_map(|capture| {
            let start = text[capture.group(2)?].parse().ok()?;
            let end = text[capture.group(3)?].parse().ok()?;

            Some(start..=end)
        })
        .flatten()
        .collect();

    Ok(numbers)
}

fn find_duplicated(numbers: Vec<u64>) -> Result<u64> {
    let duplicate_pattern = Regex::new(r"^(\d+)\1$")?;
    let sum = numbers
        .into_par_iter()
        .filter(|number| {
            let text = number.to_string();
            text.len() % 2 == 0 && duplicate_pattern.find(&text).is_some()
        })
        .sum();

    Ok(sum)
}

fn find_at_least_duplicated(numbers: Vec<u64>) -> Result<u64> {
    let duplicate_or_more_pattern = Regex::new(r"^(\d+)\1+$")?;
    let sum = numbers
        .into_par_iter()
        .filter(|number| {
            duplicate_or_more_pattern
                .find(&number.to_string())
                .is_some()
        })
        .sum();

    Ok(sum)
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs;

    #[test]
    fn part1_test() -> Result<()> {
        let input = fs::read_to_string("inputs/day02_test.txt")?;
        let data = parse_input(input)?;
        assert_eq!(find_duplicated(data)?, 1227775554);

        Ok(())
    }

    #[test]
    fn part1() -> Result<()> {
        let input = fs::read_to_string("inputs/day02.txt")?;
        let data = parse_input(input)?;
        assert_eq!(find_duplicated(data)?, 13108371860);

        Ok(())
    }

    #[test]
    fn part2_test() -> Result<()> {
        let input = fs::read_to_string("inputs/day02_test.txt")?;
        let data = parse_input(input)?;
        assert_eq!(find_at_least_duplicated(data)?, 4174379265);

        Ok(())
    }

    #[test]
    fn part2() -> Result<()> {
        let input = fs::read_to_string("inputs/day02.txt")?;
        let data = parse_input(input)?;
        assert_eq!(find_at_least_duplicated(data)?, 22471660255);

        Ok(())
    }
}
